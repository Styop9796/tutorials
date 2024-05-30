from odoo import models ,fields,api
from datetime import timedelta
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for properties'
    _order = "price desc"

    price = fields.Float(string='Offer price')
    status = fields.Selection(string='Status',
                              selection=[('accepted','Accepted'),('refused','Refused')],
                              copy=False)
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.estate_property',required=True)
    validity = fields.Integer(string='Validity(days)',default=7)
    date_deadline = fields.Date(string='Deadline',compute='_compute_date_deadline',inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.type_id',string='Property Type',store=True)

    _sql_constraints = [
        ('check_offer_price', 'CHECK( price > 0)','The offer price should be strictly postitive.')

      ]



    @api.depends('create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days



    def accept_offer(self):
        for record in self:
                if not record.property_id.state == 'offer accepted':
                    record.property_id.selling_price = record.price
                    record.property_id.buyer_id = record.partner_id
                    record.status = 'accepted'
                    record.property_id.state = 'offer accepted'
                else:
                    raise UserError("Cannot accept offer: Another offer has already been accepted.")

        return True 


    def refuse_offer(self):
        for record in self:
            record.property_id.state='offer received'
            record.status = 'refused'
        return True