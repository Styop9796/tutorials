from odoo import models ,fields,api
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name='estate.estate_property'
    _description = 'Estate properties table'
    _order = "sequence ASC , id DESC"


    name= fields.Char(string='Property name',required=True,help='Name of the property')
    description = fields.Text(string='Description of proberty')
    postcode = fields.Char(string='Postcode',required=True , help='Postcode of the property')
    date_availability = fields.Date(string='Available date',help='Available date for the property',copy=False,default= fields.Date.today() +timedelta(days=90))
    expected_price = fields.Float(string='Expected Price',required=True ,help='Expected Price of the property')
    selling_price = fields.Float(string='Sell Price',required=True, help='Selling price',readonly=False)
    bedrooms = fields.Integer(string='Bedrooms',help='Number of bedrooms',default=2)
    living_area = fields.Integer(string='Living area count',help='Number of living areas')
    facades = fields.Integer(string='Facades', help='Number of facades')
    garage = fields.Boolean(string='Garage',help='Is garage availabe')
    garden = fields.Boolean(string='Garden',help='Is garage availabe')
    garden_area = fields.Integer(string='Garden Area', help='Garden are in square meters')
    garden_orientation = fields.Selection(
                                            string='Geographical orientation',
                                            selection=[('north', 'North'), ('south', 'South'),
                                                    ('east','East'),('west','West')],
                                            help="Type is used to specify geographical orientation")

    active = fields.Boolean(default=True) 
    state = fields.Selection(selection=[('new','New'),
                                        ('offer received','Offer Received'),
                                        ('offer accepted','Offer Accepted'),
                                        ('sold','Sold'),
                                        ('canceled','Canceled')],
                                        string='Property state',
                                        default='new',
                                        copy=False,
                                        required=True
                                )
    type_id = fields.Many2one('estate.property.type',string='Property Type',help='Type of the Property',required=True)
    salesperson_id = fields.Many2one('res.users',string='Salesperson', default=lambda self:self.env.user)
    buyer_id = fields.Many2one('res.partner',string='Buyer',copy=False)
    tag_ids = fields.Many2many('estate.property.tag',string='Tags')
    offer_ids = fields.One2many('estate.property.offer','property_id',string='Offers')
    total_area = fields.Integer(string='Total area',compute='_compute_total_area')
    best_offer = fields.Float(string='Best Offer',compute='_compute_best_offer')
    sequence = fields.Integer(string='Sequence', default=1, help="Used to order stages. Lower is better.")


    _sql_constraints = [
        ('check_expected_price', 'CHECK( expected_price > 0)','The expected price should be strictly postitive.'),
         ('check_selling_price', 'CHECK( selling_price >= 0)','The expected price should be postitive.')

      ]



    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
                record.total_area=record.living_area + record.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0


    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None
            

    def set_as_sold(self): #can't set as sold if canceled
        print('gssssssssssssssssssss')

        for record in self:
            if record.state == "canceled":
                raise UserError("Can't set as sold: Record is already canceled.")
            else:
                record.state = 'sold'
                return True


    def set_as_canceled(self): # can't set as canceled if sold
        for record in self:
            if record.state=='sold':
                raise UserError("Can't set as canceled: Record is already sold")
            else:
                record.state='canceled'
                return True 
            


    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            
            ninety_percent_of_expected_price = record.expected_price * 0.9
            if float_compare(record.selling_price, ninety_percent_of_expected_price, precision_digits=2) == -1:
                raise models.ValidationError("Selling price cannot be lower than 90% of the expected price.")
            
    def action_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'view_mode': 'tree,form',
            'res_model': 'estate.property.offer',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }
    



    @api.ondelete(at_uninstall=False)
    def _prevent_delete(self):
        for record  in self:
            if record.state not in ['new', 'canceled']:
                raise UserError("You cannot delete a property that is not in 'New' or 'Canceled' state.")
            