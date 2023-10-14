# -*- coding: utf-8 -*-
# Copyright 2017, OdooTips
from __future__ import print_function
import builtins
import math
from odoo import fields, models, tools, _
import odoo.tools as tools
#forma de corregir y solucionar funciones de raiz de odoo esta es para redondeo
def float_round(value, precision_digits=None, precision_rounding=None, rounding_method='HALF-UP'):
    """Return ``value`` rounded to ``precision_digits`` decimal digits,
       minimizing IEEE-754 floating point representation errors, and applying
       the tie-breaking rule selected with ``rounding_method``, by default
       HALF-UP (away from zero).
       Precision must be given by ``precision_digits`` or ``precision_rounding``,
       not both!

       :param float value: the value to round
       :param int precision_digits: number of fractional digits to round to.
       :param float precision_rounding: decimal number representing the minimum
           non-zero value at the desired precision (for example, 0.01 for a 
           2-digit precision).
       :param rounding_method: the rounding method used: 'HALF-UP', 'UP' or 'DOWN',
           the first one rounding up to the closest number with the rule that
           number>=0.5 is rounded up to 1, the second always rounding up and the
           latest one always rounding down.
       :return: rounded float
    """
    rounding_factor = tools.float_utils._float_check_precision(precision_digits=precision_digits,
                                             precision_rounding=precision_rounding)
    if rounding_factor == 0 or value == 0:
        return 0.0

    # NORMALIZE - ROUND - DENORMALIZE
    # In order to easily support rounding to arbitrary 'steps' (e.g. coin values),
    # we normalize the value before rounding it as an integer, and de-normalize
    # after rounding: e.g. float_round(1.3, precision_rounding=.5) == 1.5
    # Due to IEE754 float/double representation limits, the approximation of the
    # real value may be slightly below the tie limit, resulting in an error of
    # 1 unit in the last place (ulp) after rounding.
    # For example 2.675 == 2.6749999999999998.
    # To correct this, we add a very small epsilon value, scaled to the
    # the order of magnitude of the value, to tip the tie-break in the right
    # direction.
    # Credit: discussion with OpenERP community members on bug 882036

    normalized_value = value / rounding_factor # normalize
    sign = math.copysign(1.0, normalized_value)
    epsilon_magnitude = math.log(abs(normalized_value), 2)
    epsilon = 2**(epsilon_magnitude-52)

    # TIE-BREAKING: UP/DOWN (for ceiling[resp. flooring] operations)
    # When rounding the value up[resp. down], we instead subtract[resp. add] the epsilon value
    # as the approximation of the real value may be slightly *above* the
    # tie limit, this would result in incorrectly rounding up[resp. down] to the next number
    # The math.ceil[resp. math.floor] operation is applied on the absolute value in order to
    # round "away from zero" and not "towards infinity", then the sign is
    # restored.

    if rounding_method == 'UP':
        normalized_value -= sign*epsilon
        rounded_value = math.ceil(abs(normalized_value)) * sign

    elif rounding_method == 'DOWN':
        normalized_value += sign*epsilon
        rounded_value = math.floor(abs(normalized_value)) * sign

    # TIE-BREAKING: HALF-UP (for normal rounding)
    # We want to apply HALF-UP tie-breaking rules, i.e. 0.5 rounds away from 0.
    else:
        normalized_value += math.copysign(epsilon, normalized_value)
        rounded_value = round(normalized_value)     # round to integer

    result = rounded_value * rounding_factor # de-normalize
    if rounding_method == 'HALF-UP':
        precision_dig = 2 if precision_rounding==0.01 else 3 if precision_rounding==0.001 else 4 if precision_rounding==0.0001 else  5 if precision_rounding==0.00001 else 6 if precision_rounding==0.000001 else 7 if precision_rounding==0.0000001 else 8 if precision_rounding==0.00000001 else 9 if precision_rounding==0.000000001 else 10 if precision_rounding==0.0000000001 else 11 if precision_rounding==0.00000000001 else 12 if precision_rounding==0.000000000001 else 2
        decimals = precision_dig if precision_digits==None else precision_digits
        multiplyWith = 10 ** decimals
        fix_round = math.floor(result * multiplyWith + 0.5) / multiplyWith
        diff = abs(fix_round-result)
        # compare = 1/multiplyWith
        if diff<0.001 and diff!=0:
            fix_round = math.floor(result * multiplyWith + 0.5) / multiplyWith
            result = fix_round
    return result
tools.float_round = float_round
