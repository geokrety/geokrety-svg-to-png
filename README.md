# GeoKrety SVG to PNG converter
Convert templates labels in SVG to PNG (or vectorized SVG).
It Also replace specific placeholders by QRCode

This is part of the GeoKrety project.

It's based  on [AI, PDF and EPS to SVG converter](https://github.com/theveloped/inkscape) by @Tobias Scheepers
itself based on [SVG to PNG converter](https://github.com/as-a-service/inkscape) by [@steren](https://twitter.com/steren)
Source on <a href="https://github.com/geokrety/geokrety-svg-to-png">GitHub</a></p>

Many thanks to:
* the [Inkscape project](https://inkscape.org/).
* [Twitter Color Emoji SVGinOT Font](https://github.com/eosrei/twemoji-color-font).

### POST parameters:

* `file`: input file added as `multipart/form-data`
* `qrcode`: The data to be encoded in the QRCode `multipart/form-data`

## Running the server locally (docker)

* Build with `docker build . -t inkscape`
* Start with `docker run -p 8080:8080 inkscape`
* Open in your browser at `http://localhost:8080"`

## Running the server locally (docker-compose)

* Run/Build using `docker-compose up --build`
* Open in your browser at `http://localhost:8080"`

# Notes
The included extension fork `render_barcode_qrcode` as it contains fixes related
to [issue](https://gitlab.com/inkscape/extensions/-/issues/280) and
[MR](https://gitlab.com/inkscape/extensions/-/merge_requests/216).
It could be removed when it will properly included in official Inkscape release.
Probably in `v1.0.1`…
