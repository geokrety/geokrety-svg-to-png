import base64
import os
import tempfile
import logging

from gevent.pywsgi import WSGIServer
from flask import Flask, after_this_request, render_template, request, send_file, abort, make_response
from subprocess import call


UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['svg'])


app = Flask(__name__)


def convert_file(input_file_path, output_dir, output_file_path, qrcode):

    call('python3 /usr/share/inkscape/extensions/render_barcode_qrcode.py --text "%s" --groupid=qrcode %s | python3 /usr/share/inkscape/extensions/geokrety_qrcode_placer.py | inkscape -p --batch-process --actions="export-filename:%s; export-plain-svg; export-text-to-path; export-dpi:300; export-area-page; export-background:white; export-background-opacity:255; export-do; FileQuit;"' %
        (qrcode, input_file_path, output_file_path), shell=True)


@app.route('/', methods=['GET', 'POST'])
def api():
    # Return UI page
    if request.method == 'GET':
        return render_template('index.html')

    # Convert file
    if request.method == 'POST':
        work_dir = tempfile.TemporaryDirectory()
        filename = 'output.'
        if request.args.get('png') is not None:
            filename += 'png'
        else:
            filename += 'svg'
        output_file_path = os.path.join(work_dir.name, filename)

        # retrieve qrcode link
        qrcode = "https://geokrety.org/en/moves"
        if request.form.get('qrcode') is not None:
            qrcode = request.form.get('qrcode')

        # check if the post request has the file part
        if 'file' not in request.files:
            logging.error("No file detected in request files")
            abort(400)

        file = request.files['file']
        if not file:
            logging.error("No file found")
            abort(400)

        if file.filename == '':
            logging.error("Filename is empty")
            abort(400)

        input_extension = file.filename.rsplit('.', 1)[1].lower()
        input_file_path = os.path.join(work_dir.name, 'input.' + input_extension)

        if input_extension not in ALLOWED_EXTENSIONS:
            logging.error("Unsupported file extension")
            abort(400)

        # Store input file to disk
        file.save(input_file_path)

        # Convert and store output file
        convert_file(input_file_path, work_dir.name, output_file_path, qrcode)

        # Delete files after conversion
        @after_this_request
        def cleanup(response):
            work_dir.cleanup()
            return response

        if os.path.exists(output_file_path):
            if request.args.get('base64') is not None:
                with open(output_file_path, 'rb') as bites:
                    response = make_response(base64.b64encode(bites.read()))
                    response.headers['Content-Transfer-Encoding'] = 'base64'
                    response.headers['mimetype'] = 'image/png'
                    return response
            else:
                return send_file(output_file_path, mimetype='image/png')

        else:
            logging.error("Could not convert file")
            return abort(500)


if __name__ == "__main__":
    http_server = WSGIServer(('', int(os.environ.get('PORT', 8080))), app)
    http_server.serve_forever()
