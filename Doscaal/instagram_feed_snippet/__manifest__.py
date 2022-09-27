# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'Instagram Feed Snippet',
    'version': '14.0.3.0',
    'summary': '''
        Wonderful app built to allow Instagram feed on your website using drag & drop snippets
        Instagram | Instagram Feed | Instagram Post | Instagram Video | Instagram Album
    ''',
    'description': """
This modules has a provision for Showing the instagram feeds inside Odoo using a simple drag and drop snippet.

- Secure Authentication

- easy configuration

- awesome snippet view

    """,
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'category': 'Website/Website',
    'depends': ['website'],
    'data': [
        'data/cron_data.xml',
        'views/assets.xml',
        'views/website_views.xml',
        'views/templates.xml'
    ],
    'images': ['static/description/banner.gif'],
    'sequence': 1,
    'installable': True,
    'price': 40,
    'currency': 'EUR'
}
