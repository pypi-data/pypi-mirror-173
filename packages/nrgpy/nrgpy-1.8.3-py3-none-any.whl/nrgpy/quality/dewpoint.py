# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 14:31:10 2020

@author: ndb
"""

import math

def calc_dp(T, RH):
    A1 = 17.625
    B1 = 243.04     #deg C
    Tdp = B1 * (math.log(RH/100) + (A1*T/(B1+T))) / (A1 - math.log(RH/100) - (A1*T/(B1+T)))
    return Tdp

