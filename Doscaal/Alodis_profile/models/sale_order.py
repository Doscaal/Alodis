
# coding: utf-8

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def __try_apply_program(self, program, coupon, status):
        res = super(SaleOrder, self).__try_apply_program(
            program, coupon, status)
        if coupon:
            coupon.write({'order_id': self.id})
        return res
