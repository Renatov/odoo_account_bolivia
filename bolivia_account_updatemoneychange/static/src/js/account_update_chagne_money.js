odoo.define('bolivia_account_updatemoneychange.ActionChangeMoney', function (require) {
	"use strict";
	var account_Change_Money = require('web.AbstractController')
	var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;
	account_Change_Money.include({
		start: function() {
			var self =this;
			var views_culminate = this._super()
			return $.when(views_culminate).then(function () {
			function UpdateMoneyChangeActionShowDialog(){
			    var cover_id = true;
			    var rpc = require('web.rpc');
			    var Dialog = require('web.Dialog');
			    var id_active_account_payment = '23'
				var dialog = new Dialog(document.body, {
			        title: "Insertar los tipos de cambios", 
			        subtitle: "Actualizar tipo de cambio",
			        size: 'medium',
			        $content: qweb.render('bolivia_account_updatemoneychange.form_money_change_popup'),
			        buttons:[{text: _t("Guardar"), name: 'button_save_money_change', classes:'oe_highlight', close: true, disabled: !cover_id, click: function () {
			        	var array = [];
			        	var datos_compañia = self.getSession();
			            $('#account_money_change_actual').each(function() {
			                var values = [];
			                $(this).find("input:not(:checkbox)").each(function(){
			                     values.push('valorcambio:'+this.value+'_idmoney:'+this.dataset.money+'_company:'+this.dataset.company+'_statusTrue:'+$(this).parent().parent().children().find('input:checkbox').is(':checked'));
			                });
			                array=values;
			            });
			            rpc.query({
				            model: 'account.account',
				            method: 'save_money_change',
				            args: [id_active_account_payment, array]
				        }) //llama a la funcion y pasa la variable a la funcion;
			        }} , {text: _t("Cancelar"), close: true, classes:'oe_link'}] 
			     });
			    dialog.open();
			    var report_get_id_comprobante = rpc.query({
		            model: 'account.account',
		            method: 'get_money_changes',
		        }).then(function (r) {
					var numbers = r;
					var option = '';
					var ckeck_money = '';
					for (var i=0;i<numbers.length;i++){
						if (numbers[i][4]==true){
							ckeck_money =  'checked'
						}
						if (numbers[i][4]==false){
							ckeck_money = ''
						}
						
					   option += '<thead><tr><th style="padding-right:20px">Moneda</th><th>Monto tipo de cambio</th><th>Tipo cambio 1 * 6,96</tr></thead><tbody><tr><th>' + numbers[i][0] + '</th><th><input data-money="'+ numbers[i][2] + '" data-company="'+ numbers[i][3] + '" value="'+ numbers[i][1] + '"></input></th><th><input type="checkbox" class="check_bolivia_change" name="all_sizes" '+ckeck_money+' style="margin-left: 46px;margin-right:auto;"></th></tr></tbody>';
					}
					$("#account_money_change_actual").append(option)
					$(document).ready(function() {
						  //set initial state.
						  $('.check_bolivia_change').click(function() {
						    if (!$(this).is(':checked')) {
						      return confirm("Si usted desactiva esta casilla la forma de ingresar el tipo de cambio es 1/6.96 debera ingresar 0.1436");
						    }
						  });
						});
				});
			   
			}
		var verif_module= ''
			if (self.initialState.model != null){
				verif_module = self.initialState.model.split('.')}
	    if (verif_module[0] == 'account'){
	    	
				var rpc = require('web.rpc');
				rpc.query({
		            model: 'account.account',
		            method: 'verificar_save_money_change',
		        }).then(function (r) { // do something 
				        	if (r==true){
				        	UpdateMoneyChangeActionShowDialog();
				        	}
					});	
				}
			});
	    return views_culminate;
	    
		},
	});
});