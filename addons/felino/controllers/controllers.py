# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class Felino(http.Controller):
    @http.route('/felino/felino', auth='public')
    def index(self, **kw):
        return "Hello, world"
    
    @http.route('/felino/dataset/<model>',type='http',auth='none',website=True)
    def indexdb(self, model,**kwargs):
        print('dataset')
        dataset=http.request.env[model].sudo().search([])
        partner_data = []
        for partner in dataset:
            partner_data.httpend({
                'id': partner.id,
                'name': partner.name,
               
                # tambahkan field lainnya yang ingin Anda tampilkan
            })
        return json.dumps(partner_data)
    
    @http.route('/felino/addon',type='http',auth='none',website=True)
    def addon(self, **kwargs):
        print('dataset')
        dataset=http.request.env['ir.module.module'].sudo().search([])
        partner_data = []
        for partner in dataset:
            partner_data.httpend({
                'id': partner.id,
                'name': partner.name,
               
                # tambahkan field lainnya yang ingin Anda tampilkan
            })
        return json.dumps(partner_data)
    
    @http.route('/felino/product', type='http', auth='none', website=True, json=True)
    def iproduct(self, **kwargs):
        if 'categ_id' in kwargs:
            categ_id = kwargs['categ_id']
            products = http.request.env['product.product'].sudo().search_read([],['id','name'])
            return json.dumps(products)
        else:
            categories = http.request.env['product.category'].sudo().search_read([], ['id', 'name','categ_id'])
            # categories = list(map(lambda x: {**x, 'child': f'/felino/product?categ_id={x["id"]}'}, categories))
            return json.dumps(categories)

    @http.route('/felino/prod', type='http', auth='none', website=True, json=True)
    def iproducta(self, **kwargs):
        if 'categ_id' in kwargs:
            categ_id = kwargs['categ_id']
            products = http.request.env['product.product'].sudo().search_read([],['id','name','categ_id'])
            return json.dumps(products)
        else:
            categories = http.request.env['product.category'].sudo().search_read([], ['id', 'name'])
            # categories = list(map(lambda x: {**x, 'child': f'/felino/product?categ_id={x["id"]}'}, categories))
            return json.dumps(categories)        
        
   

    @http.route('/felino/felino/objects', auth='public')
    def list(self, **kwargs):
        return http.request.render('felino.listing', {
            'root': '/felino/felino',
            'objects': http.request.env['felino.felino'].search([]),
        })

    @http.route('/felino/felino/objects/<model("felino.felino"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('felino.object', {
            'object': obj
        })
