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
        self.dict_instance = self.init_dict_instance()
        self.dict_assign_table = self.init_dict_assign_table()
        ### ls_instance = self.dict_instance.keys()
    def init_ls_input_port(self):
        ls_ = []
        for s in self.statement:
            if s[0]=="input":
                if s[1] == "[":
                    i = 1
                    while (s[i]!="]"):
                        i = i + 1
                    ls_.append(s[i+1])
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
                    ls_.append(s[i+1])
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
                    ls_.append(s[i+1])
                else:
                    ls_.append(s[1])
        return ls_
    def init_dict_instance(self):
        dict_ = {}
        for s in self.statement:
            if s[0] != "" and is_verilog_reserved_word(s[0]) == False:
                print s
                if s[1] == "#":
                    i = 1
                    while (s[i]!=")"):
                        i = i + 1
                    dict_[s[i+1]] = s[0]
                else :
                    dict_[s[1]] = s[0]
        return  dict_
    def init_dict_assign_table(self):
        dict_ = {}
        for iname in self.dict_instance.keys():
            for s in self.statement:
                if s[0] == iname:
                    print s[0]
        return dict_
        
if __name__ == '__main__':
    vsrc_txt = "" 
    with open("../AIMG4MLBRRP.v","r") as fp:
        for line in fp:
            vsrc_txt += line
    vsrc = Vsrc(vsrc_txt)
    print vsrc.ls_local_wire