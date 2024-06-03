from odoo import models ,fields



class EstateTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tags'
    _order = "name ASC"

    name=fields.Char(string='Property Tags',required=True)
    color = fields.Integer(string='Color', default=7)
    
    _sql_constraints = [
        ('check_tag_name', 'UNIQUE(name)','Tag exists')

      ]