# -*- coding: utf-8 -*-
import odoo
 
from odoo import http, models, fields, _
from odoo.http import request, Response
from odoo.exceptions import ValidationError, UserError
from psycopg2 import IntegrityError
import json
import logging
_logger = logging.getLogger(__name__)

class NusantechMaterialController(http.Controller):
    
    @http.route(["/api/materials"], 
    type="json", 
    auth="public", 
    methods=['GET'],
    csrf=False, 
    )
    def get_materials(self, **kwargs):
        _logger.info("trigger get_materials")
        
        material_code = request.httprequest.args.get("material_code")

        data = []
        filter = []
        if material_code:
            filter.append(('material_type','=', material_code.upper()))
        materials = request.env['ns_material.material'].sudo().search(filter)
        for material in materials:
            data.append({
                    'material_code' : material.material_code,
                    'material_name': material.material_name,
                    'material_type': material.material_type,
                    'material_buy_price': material.material_buy_price,
                    'currency': material.currency_id.name,
                    'related_supplier_id': material.related_supplier_id.id,
                    'related_supplier': material.related_supplier_id.name,
                })
        Response.status = '200'
        return {
            'code': 200,
            'status': 'success',
            'message': '',
            'data': data
        }
    
    @http.route("/api/material", 
    type="json", 
    auth="public", 
    methods=['GET'],
    csrf=False, 
    )
    def get_material(self, **kwargs):
        _logger.info("trigger get_material")
        data = None
        material_code = request.httprequest.args.get("material_code")
        
        if material_code:
            material = request.env['ns_material.material'].sudo().search([('material_code','=',material_code)])
            if material:
                data = {
                    'material_code' : material.material_code,
                    'material_name': material.material_name,
                    'material_type': material.material_type,
                    'material_buy_price': material.material_buy_price,
                    'currency': material.currency_id.name,
                    'related_supplier': material.related_supplier_id.name,
                }

                Response.status = '200'
                return {
                    'code': 200,
                    'status': 'success',
                    'message': '',
                    'data': data
                }

            else:
                Response.status = '404'
                return {
                    'code': 404,
                    'status': 'Not Found',
                    'message': 'Data not found'
                }
        else:
            Response.status = '400'
            return {
                    'code': 400,
                    'status': 'Bad Request',
                    'message': 'Invalid material code'
                }
    
    @http.route("/api/material", 
    type="json", 
    auth="public", 
    methods=['POST','PUT'],
    csrf=False, 
    )
    def create_write_material(self, **kwargs):
        _logger.info("trigger create_material")
        payload = json.loads(request.httprequest.data)
        request_method = request.httprequest.environ['REQUEST_METHOD']

        if (payload.get("material_code") is None 
            or payload.get("material_name") is None 
            or payload.get("material_type") is None
            or payload.get("material_buy_price") is None 
            or payload.get("currency") is None
            or payload.get("related_supplier_id") is None):
            
            Response.status = '400'
            return {'code': 400,'status': 'Bad Request','message': 'Invalid request data'}

        currency_id = request.env['res.currency'].sudo().search([('name','=',payload.get("currency"))]).id
    
        data = {
            'material_code': payload.get("material_code"),
            'material_name': payload.get("material_name"),
            'material_type': payload.get("material_type"),
            'material_buy_price': payload.get("material_buy_price"),
            'currency_id': currency_id,
            'related_supplier_id': payload.get("related_supplier_id"),
        }

        try:
            if (request_method == 'PUT'):
                _logger.info("trigger update")
                old_data = request.env["ns_material.material"].sudo().search([('material_code','=',data.get("material_code"))]) 
                
                if old_data:
                    old_data.update(data)
                    request.env["ns_material.material"].sudo().write(old_data) 
                    Response.status = '200'
                    return {'code': 200,'status': 'Success','message': 'Data updated successfully.'}
                else:
                    Response.status = '404'
                    return {'code': 404,'status': 'Not Found','message': 'Data not found.'}
            else:
                _logger.info("trigger create")
                request.env["ns_material.material"].sudo().create(data) 
                Response.status = '200'
                return {'code': 200,'status': 'Success','message': 'Data created successfully.'}
            
        except ValidationError as e:
            _logger.error(e)
            http.request._cr.rollback()
            Response.status = '400'
            return {'code': 400,'status': 'Bad Request','message': e}
        except IntegrityError as e:
            _logger.error(e)
            http.request._cr.rollback()
            Response.status = '500'
            return {'code': 400,'status': 'Bad Request','message': e}
        except Exception as e:
            _logger.error(e)
            http.request._cr.rollback()
            Response.status = '500'
            return {'code': 500,'status': 'Internal Server Error','message': e}

    @http.route("/api/material", 
    type="json", 
    auth="public", 
    methods=['DELETE'],
    csrf=False, 
    )
    def delete_material(self, **kwargs):
        _logger.info("trigger delete_material")
        data = None
        material_code = request.httprequest.args.get("material_code")
        
        if material_code:
            material = request.env['ns_material.material'].sudo().search([('material_code','=',material_code)])
            if material:
                try:
                    material.unlink()
                    Response.status = '200'
                    return {'code': 200,'status': 'Success','message': 'Data deleted successfully.'}
                except Exception as e:
                    _logger.error(e)
                    http.request._cr.rollback()
                    Response.status = '500'
                    return {'code': 500,'status': 'Internal Server Error','message': e}
            else:
                Response.status = '500'
                return {'code': 400,'status': 'Bad Request','message': 'Invalid material_code value or not found.'}
        else:
            Response.status = '500'
            return {'code': 400,'status': 'Bad Request','message': 'Please provide material_code parameter.'}

  