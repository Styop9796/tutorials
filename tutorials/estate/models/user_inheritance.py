from odoo import fields, models




class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.estate_property','salesperson_id',string="Properties",
                                    domain="[('salesperson_id', '=', id)]"  # Domain to filter available properties
)