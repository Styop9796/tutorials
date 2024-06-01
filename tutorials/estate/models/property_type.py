from odoo import models ,fields, api


class PropertyType(models.Model):

    _name='estate.property.type'
    _description = 'Estate property types'
    _order = "name ASC"


    name = fields.Char(string='Property Type',required=True)
    property_ids = fields.One2many('estate.estate_property','type_id',string='Properties')
    offer_ids = fields.One2many('estate.property.offer',inverse_name='property_type_id',string='Offers')
    offer_count = fields.Integer(string='Offer Count',compute='_compute_offer_count',store = True)


    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)','Type exists')

      ]
    



    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            offers = record.property_ids.mapped('offer_ids')
            record.offer_count = len(offers)
