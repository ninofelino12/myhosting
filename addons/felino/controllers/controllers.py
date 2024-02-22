# -*- coding: utf-8 -*-
from odoo import http


class Felino(http.Controller):
    @http.route('/felino/felino', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/felino/felino/objects', auth='public')
    def list(self, **kw):
        return http.request.render('felino.listing', {
            'root': '/felino/felino',
            'objects': http.request.env['felino.felino'].search([]),
        })

    @http.route('/felino/felino/objects/<model("felino.felino"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('felino.object', {
            'object': obj
        })
