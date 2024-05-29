from odoo import models ,fields


class PropertyType(models.Model):

    _name='estate.property.type'
    _description = 'Estate property types'


    name = fields.Char(string='Property Type',required=True)



    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)','Type exists')

      ]