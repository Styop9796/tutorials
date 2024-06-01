from odoo import fields,models




class EstatePropertyInherit(models.Model):
    _inherit="estate.estate_property"

    def set_as_sold(self):
        print(self.buyer_id)
        print(type(self.buyer_id))

        values = {'partner_id':self.buyer_id.id,
                 'move_type' : 'out_invoice',
                 'journal_id':1}
        self.env['account.move'].create(values)
        print('gogogo')
        return super().set_as_sold()
    

