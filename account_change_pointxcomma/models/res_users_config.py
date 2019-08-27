# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV
# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# example use  self.env.user.notify_info('My information message')
from odoo import api, fields, models, _

class ResUsers(models.Model):
    _inherit = 'res.users'
    cambio_puntoxcoma = fields.Boolean(sring="Cambiar punto por coma en teclado numerico")
    key_code_punto = fields.Text(sring="Presione la tecla . a cambiar")
    
    def get_key_press(self, user_id=False):
        key_code_punto = self.cambio_puntoxcoma
        cambio_puntoxcoma = self.key_code_punto
        return key_code_punto, cambio_puntoxcoma