from odoo import models ,fields



class EstateTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tags'

    name=fields.Char(string='Property Tags',required=True)