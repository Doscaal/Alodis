
# coding: utf-8

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if res:
            for rec in self:
                wallet = rec.order_line.mapped('coupon_id').filtered(
                    lambda lc: lc.program_id.influencer_id
                ).program_id.influencer_id
                if len(wallet) == 1:
                    gain = rec.amount_untaxed * wallet.cashback
                wallet.write({
                    'balance': wallet.balance + gain
                })
        return res

    def __try_apply_program(self, program, coupon, status):
        res = super(SaleOrder, self).__try_apply_program(
            program, coupon, status)
        if coupon:
            coupon.write({'order_id': self.id})
        return res
