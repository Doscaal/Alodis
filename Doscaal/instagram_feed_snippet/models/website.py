# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

import requests
from werkzeug import urls
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Website(models.Model):
    _inherit = "website"

    instagram_app_id = fields.Char(string='Instagram App ID')
    instagram_app_secret = fields.Char(string='Instagram App Secret')
    instagram_access_token = fields.Char(string='Instagram Access Token', readonly=True, store=True)
    instagram_token_expire_date = fields.Datetime(string='Instagram Token Expire Timestamp', readonly=True, store=True)
    instagram_row = fields.Integer(string='No. of Posts Per Row', default=4)
    instagram_token_state = fields.Selection([('draft', 'Draft'), ('valid', 'Valid'), ('expired', 'Expired'), ('error', 'Error')], string='Status', default='draft', readonly=True, store=True)
    instagram_error_message = fields.Text('Instagram Error Message', readonly=True, store=True)
    user_picture = fields.Binary('User Picture')
    slider_speed = fields.Integer(string='Slider Delay Speed', default=5000)
    instagram_number_of_row = fields.Integer(string='No. Of Initial Row', default=1)
    instagram_feed_design = fields.Selection([('grid', 'Grid'), ('slider', 'Slider')], string='Instagram Feed Design', default='grid', required=True, store=True)

    @api.constrains('instagram_number_of_row', 'instagram_feed_design')
    def _check_row_value(self):
        if self.instagram_feed_design == 'grid':
            if self.instagram_number_of_row > 6 or self.instagram_number_of_row < 1:
                raise ValidationError(_('Enter Value of Number Of Row Between 1-6.'))

    @api.constrains('instagram_row')
    def _check_no_of_post_per_row_value(self):
        if self.instagram_row > 6 or self.instagram_row < 2:
            raise ValidationError(_('Enter Value of No of Posts Per Row Between 2-6.'))

    @api.model
    def _refresh_instagram_long_lived_token(self):
        self = self.env['website'].search([('instagram_access_token', '!=', False), ('instagram_app_secret', '!=', False), ('instagram_token_expire_date', '>', fields.Datetime.now())])
        for website in self:
            url = "https://graph.instagram.com/refresh_access_token"
            params = {
                'grant_type': 'ig_refresh_token',
                'access_token': website.instagram_access_token
            }
            response = requests.request("GET", url, params=params)
            if response.status_code == 200:
                instagram_token_expire_date = fields.Datetime.now() + timedelta(seconds=response.json().get('expires_in') - 300)
                website.sudo().write({
                    'instagram_access_token': response.json().get('access_token'),
                    'instagram_token_expire_date': instagram_token_expire_date,
                    'instagram_token_state': 'valid',
                    'instagram_error_message': ''
                })
            else:
                website.sudo().write({
                    'instagram_token_state': 'error',
                    'instagram_error_message': response.json().get('error_message')
                })

    def authorize_instagram_for_token(self):
        url_params = urls.url_encode({
            'client_id': self.instagram_app_id,
            'redirect_uri': urls.url_join(self.get_base_url(), '/instagram/token/redirect'),
            'scope': 'user_profile,user_media',
            'response_type': 'code',
            'state': self.id
        })
        url = "https://api.instagram.com/oauth/authorize?%s" % url_params
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': url,
        }
