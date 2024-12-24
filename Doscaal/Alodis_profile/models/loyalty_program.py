# coding: utf-8

from odoo import models, fields


class LoyaltyProgram(models.Model):
    _inherit = 'loyalty.program'


    influencer_id = fields.Many2one(comodel_name='loyalty.card',
                                    string='Wallet influencer')
