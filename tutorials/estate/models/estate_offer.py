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
    
    @api.model_create_multi
    def create(self, vals_list):
        property_ids_with_lower_price = []
        for new_record in vals_list:
            property_id = new_record.get('property_id')
            if property_id:
                property_id = int(property_id)
                existing_offer = self.env['estate.property.offer'].search([('property_id', '=', property_id)], order='price desc', limit=1)
        
            if existing_offer and new_record.get('price', 0) <= existing_offer.price:
                # Store property_id with lower priced offers in a list
                property_ids_with_lower_price = [existing_offer.property_id.id]
            
        if property_ids_with_lower_price:
            # Raise an error if there are offers with lower prices
            raise UserError("Cannot create offer: The price should be higher than the existing offer.")
        
        # Set property state to 'offer received' for all new records
        property_objs = self.env['estate.estate_property'].browse(property_id for vals in vals_list)
        property_objs.state=  'offer received'
        
        # Create the offers
        return super(PropertyOffer, self).create(vals_list)
