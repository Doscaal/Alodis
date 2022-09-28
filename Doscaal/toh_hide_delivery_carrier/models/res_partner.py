import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = "res.partner"
    
    tipo_cliente = fields.Selection([ ('b2c', 'B2C'),('b2b', 'B2B'),],'Tipo de Cliente')#, default='b2c') 