from odoo import fields,models
from odoo import Command




class EstatePropertyInherit(models.Model):
    _inherit="estate.estate_property"

    def set_as_sold(self):
        print(self.buyer_id)
        print(type(self.buyer_id))

        values = {'partner_id':self.buyer_id.id,
                 'move_type' : 'out_invoice',
                 'journal_id':1,
                
                 'invoice_line_ids': [
            Command.create({
                'name': self.name,
                'quantity': 1,  
                'price_unit': self.selling_price * 0.06 + 100.00, 
                'account_id': 1 # ????????????
            })
        ],
                 }
        self.env['account.move'].create(values)
        print('gogogo')
        return super().set_as_sold()
    

