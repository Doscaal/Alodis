# coding: utf-8

from odoo import models, fields, api


class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'

    amount_total = fields.Monetary(string="Total TTC", compute="compute_ttc")
    amount_untaxed = fields.Monetary(string="Total HT", compute="compute_ht")
    state_order = fields.Selection(related="order_id.state")
    date_order = fields.Datetime(string="Date de commande",
                                 compute="compute_date")
    currency_id = fields.Many2one(related="order_id.currency_id")

    @api.depends('order_id')
    def compute_ttc(self):
        for rec in self:
            rec.amount_total = rec.order_id.state in (
                'sale', 'done') and rec.amount_total or 0

    @api.depends('order_id')
    def compute_ht(self):
        for rec in self:
            rec.amount_untaxed = rec.order_id.state in (
                'sale', 'done') and rec.amount_untaxed or 0

    @api.depends('order_id')
    def compute_date(self):
        for rec in self:
            rec.date_order = rec.order_id.state in (
                'sale', 'done') and rec.date_order or False
