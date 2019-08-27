odoo.define('account_change_pointxcomma.AccountChangePointXcomma', function (require) {
	"use strict";
	var account_Change_Money = require('web.AbstractController')
	var AbstractWebClient = require("web.AbstractWebClient");
	var core = require('web.core');
	var basic_field = require('web.basic_fields');
	var mixins = require('web.mixins');
	var new_value_form_input_id = require('web.FormRenderer')
    var start, end;
	var KeyboardNavigationCommaAltMixin = {

			init: function () {
				this._super();
				var rpc = require('web.rpc');
				this.true_key_num ="";
				this.key_numpad_coma_code = "";
				var self = this
				var context_change = this.getSession().user_context
				rpc.query({
                    model: 'res.users',
                    method: 'get_key_press',
                    args: [context_change.uid]
                }).then(function (returned_value) {
                	self.key_numpad_coma_code = returned_value[1];
                	self.true_key_num = returned_value[0];
                    });
			},
			_convertCharToGreek: function (charStr) {
				return charStr == "." ? "," : charStr;
			},
	        _commaPressed: function (keyEvent) {
	        	var config = require('web.config');
	        	if (keyEvent.view){
	        		if (keyEvent.view.event){
	        	var evt = keyEvent.view.event
	        	var val = keyEvent.target.value;
	        	keyEvent.target.comma_true =true;
	        	keyEvent.target.comma_search = false
	        	_.each(keyEvent.target.classList, function (class_name) {
	        		if (class_name=='o_field_float'||class_name=='o_field_number'||class_name=='o_input'){
	        			keyEvent.target.comma_true =true;
	        		}
	        		if (class_name=='ui-autocomplete-input'||class_name=='o_searchview_input'||class_name=='form-control'||keyEvent.target.parentNode.className=='o_searchview_extended_prop_value'){
	        			keyEvent.target.comma_search = true
	        		}
	        	});
	        	keyEvent.target.value_old = false;
	            var charCode = (typeof evt.which == "undefined") ? evt.keyCode : evt.which;
	        	if (charCode==this.key_numpad_coma_code && keyEvent.target.name!="key_code_punto" && this.true_key_num==true && keyEvent.target.comma_true==true) {
	                var charStr = ",";
	                start = keyEvent.target.selectionStart;
	                end = keyEvent.target.selectionEnd;
	                if (start >-1|| end >-1){
	                	keyEvent.target.value = val.slice(0, start) + charStr + val.slice(end);
	                }
	                
	                keyEvent.target.focus();
	                var caretPos = start + charStr.length;
//	                keyEvent.target.setSelectionRange(start, end); keyEvent.preventDefault();
	                keyEvent.target.caretPos = caretPos;
	                if(caretPos){
	                keyEvent.target.setSelectionRange(caretPos, caretPos);
	                }
	                keyEvent.target.value_old = keyEvent.target.value;
	                if (keyEvent.target.comma_search == true){
	                	keyEvent.preventDefault();
	                }
	                return keyEvent;
	            }
	        	if (keyEvent.target.name=="key_code_punto" && charCode!=8) {
	        		if (keyEvent.keyCode){
	                var charStr = keyEvent.keyCode;
	        		}else{
	        		var charStr = keyEvent.which;
	        		}
	                start = keyEvent.target.selectionStart;
	                end = keyEvent.target.selectionEnd;
	                keyEvent.target.value = charStr;
	                keyEvent.target.focus();
	                var caretPos = start + charStr.length;
	                keyEvent.target.setSelectionRange(caretPos, caretPos);
	                keyEvent.target.value_old = charStr;
	                keyEvent.target.comma_true =true;
	                return keyEvent;
	            }
	            var alt = keyEvent.altKey || keyEvent.key === "Alt",
	                newEvent = _.extend({}, keyEvent),
	                shift = keyEvent.shiftKey || keyEvent.key === "Shift";
	            // Mock event to make it seem like Alt is not pressed
	            if (alt && !shift) {
	                newEvent.altKey = false;
	                if (newEvent.key === "Alt") {
	                    newEvent.key = "Shift";
	                }
	            }
	            return newEvent;
	        	}
	        		}
	        	else {
	        	return keyEvent;
	        	}
	        },

	        _onKeyDown: function (keyDownEvent) {
	            return this._super(this._commaPressed(keyDownEvent));
	        },
	    };
	    AbstractWebClient.include(KeyboardNavigationCommaAltMixin);
	    basic_field.InputField.include({
	    	_onInput: function () { //Lugar donde se actualiza la coma despues de que pasa por proxy(_onInput) de mixins
	    		var ssup=this._super()
	    		if(this.$input[0]){
	    		if(this.$input[0].value_old && this.$input[0].comma_true==true){
	    			this.$input[0].value=this.$input[0].value_old;
	    			this.$input[0].focus();
	    			this.$input[0].setSelectionRange(this.$input[0].caretPos, this.$input[0].caretPos);
	    		}
	    		}
	    	}
	    })
});