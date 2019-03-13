from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time, pytz
from datetime import datetime 
class AccountAccount(models.Model):
    _inherit = 'account.account'

    @api.model 
    def get_money_changes(self):
        currencys = self.env['res.currency'].search([('active','=',True),('id','!=',self.env.user.company_id.currency_id.id)])
        currency_company = self.env['res.currency'].search([('active','=',True),('id','=',self.env.user.company_id.currency_id.id)])
        data_money = []
        for currency in currencys:
            company_id=self.env.user.company_id.id
            time_compare = time.strftime('%Y-%m-%d %H:%M:%S')
            hora_factura_bolivia = datetime.strptime(time_compare, "%Y-%m-%d %H:%M:%S")
            fecha_zona =  str(self._covertir_fecha_hora_zona(hora_factura_bolivia, True))
            compare_time_change = self.env['res.currency.rate'].search(['&', ('currency_id','=',currency.id),('company_id','=',self.env.user.company_id.id)], order="create_date desc, id desc", limit=1)
            if len(compare_time_change) > 0:
                if compare_time_change.rate_mayor_a_uno ==True:
                    currency_rate = round(currency_company.rate / currency.rate, 5)
                else:
                    currency_rate = currency.rate
                if compare_time_change.create_date==False or (currency.date==False or compare_time_change.create_date.strftime('%Y-%m-%d') < fecha_zona):
                    data_money.append((currency.name, currency_rate, currency.id, company_id, compare_time_change.rate_mayor_a_uno))
            else:
                currency_rate = currency.rate
                data_money.append((currency.name, currency_rate, currency.id, company_id, True))
                
        return data_money
    @api.model
    def verificar_save_money_change(self):
        verif_currencys = self.env['res.currency'].search([('active','=',True),('id','!=',self.env.user.company_id.currency_id.id)])
        time_compare = time.strftime('%Y-%m-%d %H:%M:%S')
        hora_factura_bolivia = datetime.strptime(time_compare, "%Y-%m-%d %H:%M:%S")
        fecha_zona =  str(self._covertir_fecha_hora_zona(hora_factura_bolivia, True))
        for currency in verif_currencys:
            compare_time_change = self.env['res.currency.rate'].search(['&', ('currency_id','=',currency.id),('company_id','=',self.env.user.company_id.id)], order="create_date desc, id desc", limit=1)
            if compare_time_change.create_date==False or compare_time_change.create_date.strftime('%Y-%m-%d') <fecha_zona:
                x=True
                break
            else:
                x=False
        return x
    @api.model
    def save_money_change(self, money_id, datos):
        currency_company = self.env['res.currency'].search([('active','=',True),('id','=',self.env.user.company_id.currency_id.id)])
        for dato_money in datos:
            datos_money = dato_money.split('_')
            guardar_valor = datos_money[0].split(':')
            comprobar_cambio =  guardar_valor[1].replace(',', '.')
            comprobar_cambio1 =  comprobar_cambio.replace('.', '')
            if not comprobar_cambio1.isdigit():
                raise UserError(_('La cifra para cambio de moneda solo puede tener numeros.'))
            guardar_id = datos_money[1].split(':')
            guardar_company = datos_money[2].split(':')
            guardar_statusTrue = datos_money[3].split(':')
            time_save = time.strftime('%Y-%m-%d %H:%M:%S')
            if guardar_statusTrue[1]=='true':
                guardar_statusTrue[1]=True
                comprobar_cambio = currency_company.rate / float(comprobar_cambio)
            if guardar_statusTrue[1]=='false':
                guardar_statusTrue[1]=False
            hora_bolivia = datetime.strptime(time_save, "%Y-%m-%d %H:%M:%S")
            fecha_zona =  str(self._covertir_fecha_hora_zona(hora_bolivia, True))
            self.env['res.currency.rate'].sudo().create({'name': hora_bolivia,
            'rate': comprobar_cambio,
            'currency_id': guardar_id[1],
            'company_id': guardar_company[1],
            'rate_mayor_a_uno': guardar_statusTrue[1]})
        x=1
        return x
    def _covertir_fecha_hora_zona(self, date_zone, solo_fecha=False):
        time_zone= self.env.user.tz
        if time_zone==False:
            raise UserError(_('Configure bien el usuario no tiene fecha de zona'))
        tz = pytz.timezone(time_zone)
        time_zone = tz.utcoffset(date_zone)
        create_date = date_zone + time_zone
        if solo_fecha == True:
            create_date = create_date.date()           
        return create_date
    
class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'
    
    rate_mayor_a_uno  = fields.Boolean(
        string='Cambio mayor a uno',
        help='Use esta opcion si quiere que el calculo sea mayor a 1',
        store=True)