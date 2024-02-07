# coding: utf-8

from odoo import models, fields


class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'

    amount_total = fields.Monetary(related="order_id.amount_total")
    amount_untaxed = fields.Monetary(related="order_id.amount_untaxed")
    state_order = fields.Selection(related="order_id.state")
    date_order = fields.Date(related="order_id.date_order")
    currency_id = fields.Many2one(related="order_id.currency_id")
