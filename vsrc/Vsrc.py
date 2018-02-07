# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 22:52:57 2018

@author: ryotakata
"""
import sys
import csv
from constructor_funcs import trans_vsrc_to_ls2d
from is_verilog_reserved_word import is_verilog_reserved_word

class Vsrc:
    def __init__(self,vsrc_txt):
        self.statement = trans_vsrc_to_ls2d(vsrc_txt)
        self.module_name = self.statement[0][1]
        self.ls_input_port = self.init_ls_input_port()
        self.ls_output_port = self.init_ls_output_port()
        self.ls_local_wire = self.init_ls_local_wire()
        self.dict_instance, self.dict_param, self.dict_statement = self.init_dict_instance()
        ### ls_instance = self.dict_instance.keys()
    def init_ls_input_port(self):
        ls_ = []
        for s in self.statement:
            if s[0]=="input":
                if s[1] == "[":
                    i = 1
                    while (s[i]!="]"):
                        i = i + 1
                    range_ = reduce(lambda x, y : x + y, s[1:i+1])
                    ls_.append(s[i+1]+range_)
                else:
                    ls_.append(s[1])
        return ls_
    def init_ls_output_port(self):
        ls_ = []
        for s in self.statement:
            if s[0]=="output":
                if s[1] == "[":
                    i = 1
                    while (s[i]!="]"):
                        i = i + 1
                    range_ = reduce(lambda x, y : x + y, s[1:i+1])
                    ls_.append(s[i+1]+range_)
                else:
                    ls_.append(s[1])
        return ls_
    def init_ls_local_wire(self):
        ls_ = []
        for s in self.statement:
            if s[0]=="wire":
                if s[1] == "[":
                    i = 1
                    while (s[i]!="]"):
                        i = i + 1
                    range_ = reduce(lambda x, y : x + y, s[1:i+1])
                    ls_.append(s[i+1]+range_)
                else:
                    ls_.append(s[1])
        return ls_
    def init_dict_instance(self):
        dict_inst = {}
        dict_param = {}
        dict_statement = {}
        for s in self.statement:
            if s[0] != "" and is_verilog_reserved_word(s[0]) == False:
                if s[1] == "#":
                    i = 1
                    while (s[i]!=")"):
                        i = i + 1
                    dict_inst[s[i+1]] = s[0]
                    dict_param[s[i+1]] = s[2:i+1]
                    dict_statement[s[i+1]] = s[i+2:]
                else :
                    dict_inst[s[1]] = s[0]
                    dict_param[s[1]] = ""
                    dict_statement[s[1]] = s[2:]
        return  dict_inst, dict_param, dict_statement