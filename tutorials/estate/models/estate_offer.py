from odoo import models ,fields



class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for properties'

    price = fields.Float(string='Offer price')
    status = fields.Selection(string='Status',
                              selection=[('accepted','Accepted'),('refused','Refused')],
                              copy=False)
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.estate_property',required=True)
