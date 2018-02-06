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


class Wapvsrc(Vsrc):
    def __init__(self, vsrc, dict_vsrc):
        self.statement = vsrc.statement
        self.module_name = vsrc.module_name
        self.ls_input_port = vsrc.ls_input_port
        self.ls_output_port = vsrc.ls_output_port
        self.ls_local_wire = vsrc.ls_local_wire
        self.dict_instance = self.__mask_dict_instance(vsrc, dict_vsrc)
        self.dict_param = vsrc.dict_param
        self.dict_statement = vsrc.dict_statement
        self.dict_vsrc = dict_vsrc
        self.dict_wire_table = self.init_dict_wire_table()
    def __mask_dict_instance(self, vsrc, dict_vsrc):
        dict_ = {}
        print vsrc.dict_instance
        for key in vsrc.dict_instance.keys():
            value = vsrc.dict_instance[key]
            print key, value
            if len([m for m in dict_vsrc.keys() if m == value]) > 0:
                dict_[key] = value
        return dict_
    def init_dict_wire_table(self):
        dict_ = {}
        for iname in self.dict_instance.keys():
            vsrc = self.dict_vsrc[self.dict_instance[iname]]
            dict_[iname] = self.__gen_wire_table(vsrc, self.dict_statement[iname])
        return dict_
    def __gen_wire_table(self, vsrc, stat):
        wire_table = {}
        in_wire_table = {}
        out_wire_table = {}     
        io_wire_table = self.__gen_io_wire_table(stat)
        for wire in io_wire_table.keys():
            port = io_wire_table[wire]
            if self.__is_input_port(vsrc,port):
                in_wire_table[wire] = port
            elif self.__is_output_port(vsrc,port):
                out_wire_table[wire] = port
            else:
                assert False
        wire_table["in"] = in_wire_table
        wire_table["out"] = out_wire_table
        return wire_table
    def __gen_io_wire_table(self, stat):
        io_wire_table = {}
        assert stat[0] == "("
        assert stat[-1] ==")"
        stat = stat[1:-1]
        p = "port"
        value = ""
        for s in stat:
            if p == "port":
                value = s
                p = "("
            elif p == "(":
                p = "wire"
            elif p == "wire":
                io_wire_table[s]= value
                value = ""
                p = ")"
            elif p == ")":
                p = "port"
        return io_wire_table
    def __is_input_port(self, vsrc, str_):
        if len([s for s in ["." + i for i in vsrc.ls_input_port] if s == str_]) > 0:
            return True
        else:
            return False
    def __is_output_port(self, vsrc, str_):
        if len([s for s in ["." + i for i in vsrc.ls_output_port] if s == str_]) > 0:
            return True
        else:
            return False

if __name__ == '__main__':
    vsrc_txt = "" 
    with open("../AIMG4MLBRRP.v","r") as fp:
        for line in fp:
            vsrc_txt += line
    vsrc = Vsrc(vsrc_txt)