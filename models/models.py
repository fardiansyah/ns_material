# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError


class NusantechMaterial(models.Model):
    _name = 'ns_material.material'
    _description = 'Material Model'
    _sql_constraints = [

        ('ns_material_material_code_uniq', 'unique (material_code)', "Code already exists!"),

    ]

    _rec_name = 'material_code'

    material_code = fields.Char('Material Code', required=True)
    material_name = fields.Char('Material Name', required=True)
    material_type = fields.Selection([
        ('F','Fabric'),
        ('J','Jeans'),
        ('C','Cotton')
    ], default='F', required=True)
    material_buy_price = fields.Monetary(
        string="Material Buy Price", currency_field='currency_id', required=True)
    currency_id = fields.Many2one(
        string="Currency", comodel_name='res.currency', required=True)
    related_supplier_id = fields.Many2one('res.partner', string='Related Supplier', required=True)

    @api.constrains('material_buy_price')
    def _check_material_buy_price(self):
        if self.material_buy_price < 100:
            raise ValidationError("Field Material Buy Price can't be less than 100")
    
