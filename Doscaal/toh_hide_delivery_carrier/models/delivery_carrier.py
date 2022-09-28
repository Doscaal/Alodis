import logging

from odoo import models, fields, api
from odoo.exceptions import UserError
from ast import literal_eval

_logger = logging.getLogger(__name__)

class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    
    aplica_tipo_cliente = fields.Selection([ ('b2c', 'B2C'),('b2b', 'B2B'),],'Aplica para cliente') #, default='b2c')
    
# =====================================================================
#   _MATCH_ADDRESS(SELF, PARTNER)
#   Permite ocultar el proveedor de acuerdo a ciertas condiciones
# =====================================================================    
    def _match_address(self, partner):
        res = super(DeliveryCarrier, self)._match_address(partner)

        #Si cliente no tiene configurado nada en campo tipo_cliente
        #o método de envio no tiene configurado nada en campo aplica_tipo_cliente
        if not self.aplica_tipo_cliente or not partner.tipo_cliente:
            return res

        #En caso de que tanto cliente como método de envío tengan configurado algo
        #No mostrar si tienen diferentes valores
        elif self.aplica_tipo_cliente != partner.tipo_cliente:
            return False

        return res