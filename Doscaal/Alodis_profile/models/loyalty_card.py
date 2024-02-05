# coding: utf-8

from odoo import models, fields


class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'

    amount_total = fields.Monetary(related="order_id.amount_total")
    amount_untaxed = fields.Monetary(related="order_id.amount_untaxed")
    state_order = fields.Selection(related="order_id.state")
