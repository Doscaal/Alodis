# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

import requests
import werkzeug
from werkzeug import urls
from datetime import timedelta

from odoo import fields, http
from odoo.http import request


class WebsiteSale(http.Controller):
    @http.route(['/get/instagram/credentials'], type='json', auth="public", website=True)
    def get_instagram_credentials(self, **kwargs):
        website = request.env['website'].sudo().search([('id', '=', kwargs.get('website_id'))])
        vals = {
            'instagram_access_token': website.instagram_access_token,
            'instagram_row': website.instagram_row,
            'user_picture': website.user_picture,
            'instagram_feed_design': website.instagram_feed_design,
            'slider_speed': website.slider_speed,
            'instagram_number_of_row': website.instagram_number_of_row,
        }
        return vals

    def _get_instagram_long_lived_token(self, client_secret, access_token):
        url = "https://graph.instagram.com/access_token"
        params = {
            'grant_type': 'ig_exchange_token',
            'client_secret': client_secret,
            'access_token': access_token
        }
        response = requests.request("GET", url, params=params)
        if response.status_code == 200:
            instagram_token_expire_date = fields.Datetime.now() + timedelta(seconds=response.json().get('expires_in') - 300)
            return {
                'instagram_access_token': response.json().get('access_token'),
                'instagram_token_expire_date': instagram_token_expire_date,
                'instagram_token_state': 'valid',
                'instagram_error_message': ''
            }
        else:
            return {
                'instagram_token_state': 'error',
                'instagram_error_message': response.json().get('error').get('error_user_msg')
            }

    @http.route(['/instagram/token/redirect'], type='http', auth="public", website=True)
    def get_instagram_token_redirect(self, **kwargs):
        if kwargs.get('code'):
            website = request.env['website'].sudo().browse(int(kwargs.get('state')))
            url = "https://api.instagram.com/oauth/access_token"
            payload = {
                'client_id': website.instagram_app_id,
                'client_secret': website.instagram_app_secret,
                'grant_type': 'authorization_code',
                'redirect_uri': urls.url_join(website.get_base_url(), '/instagram/token/redirect'),
                'code': kwargs.get('code')
            }
            response = requests.request("POST", url, data=payload)
            if response.status_code == 200:
                token_data = self._get_instagram_long_lived_token(website.instagram_app_secret, response.json().get('access_token'))
                website.sudo().write(token_data)
            else:
                website.sudo().write({
                    'instagram_token_state': 'error',
                    'instagram_error_message': response.json().get('error_message')
                })
        action = request.env.ref('website.action_website_list').sudo()
        redirect_url = urls.url_join(website.get_base_url(), '/web#id=%s&model=website&view_type=form&action=%s' % (website.id, action.id))
        return werkzeug.utils.redirect(redirect_url)
