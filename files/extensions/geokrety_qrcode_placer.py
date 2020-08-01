#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2020 Mathieu Alorent (https://geokrety.org/)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110, USA.
#
"""
Provide the GeoKrety QR Code placer.
"""

from __future__ import print_function

from itertools import product

import inkex
from inkex import Group, Rectangle, Use, PathElement
from inkex.transforms import Transform


class GeokretyQrCodePlacer(inkex.Effect):
    """Generate QR Code Extension"""
    def add_arguments(self, pars):
        pars.add_argument("--placeholderid", default='placeholderQR')
        pars.add_argument("--qrcodeid", default='qrcode')

    def effect(self):

        opt = self.options

        if not opt.placeholderid:
            raise inkex.AbortExtension('Please enter the placeholder ID')
        elif not opt.qrcodeid:
            raise inkex.AbortExtension('Please enter the QRCode ID')

        placeholder = self.svg.getElementById(opt.placeholderid)
        qrcode = self.svg.getElementById(opt.qrcodeid)

        if placeholder is None or qrcode is None:
            # Delete the generated qrcode
            qrcode.getparent().remove(qrcode)
            return

        # Reset scale before processing
        qrcode.set('transform', 'scale(1,1)')

        # Get scaling factors
        scalex = placeholder.bounding_box().width  / qrcode.bounding_box().width
        scaley = placeholder.bounding_box().height / qrcode.bounding_box().height

        # Apply scaling and translating
        tr = Transform()
        tr.add_translate(placeholder.bounding_box().left, placeholder.bounding_box().top)
        qrcode.set('transform', tr)
        tr.add_scale(scalex, scaley)
        qrcode.set('transform', tr)

        # Move qrcode inplace of the placeholder
        placeholder.getparent().append(qrcode)

        # Delete the placeholder
        placeholder.getparent().remove(placeholder)

    def has_changed(self, ret):
        # Always update the dociument
        return True


if __name__ == '__main__':
    GeokretyQrCodePlacer().run()
