from odoo import fields,models




class EstatePropertyInherit(models.Model):
    _inherit="estate.estate_property"
    _description = 'Invoice management'



    new_one = fields.Boolean('test', defaul=False)
    new_on2212112e = fields.Boolean('test', defaul=False)


    def set_as_sold(self):
        values = {'partner_id':self.partner_id,
                 'move_type' : 'out_invoice'}
        self.env['account.move'].create(values)
        print('gogogo')
        return super().set_as_sold()
    

