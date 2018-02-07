#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:49:51 2018

@author: ryotakata
"""

from operator import itemgetter
from Vsrc import Vsrc
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
        for key in vsrc.dict_instance.keys():
            value = vsrc.dict_instance[key]
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
        from constructor_funcs import is_input_port
        from constructor_funcs import is_output_port
        wire_table = {}
        in_wire_table = {}
        out_wire_table = {}     
        io_wire_table = self.__gen_io_wire_table(stat)
        for wire in io_wire_table.keys():
            port = io_wire_table[wire]
            if is_input_port(vsrc,port):
                in_wire_table[wire] = port
            elif is_output_port(vsrc,port):
                out_wire_table[wire] = port
            else:
                print wire, port, vsrc.module_name
                assert False
        wire_table["in"] = in_wire_table
        wire_table["out"] = out_wire_table
        return wire_table
    def __gen_io_wire_table(self, stat):
        io_wire_table = {}
        assert stat[0] == "("
        assert stat[-1] ==")"
        stat = stat[1:-1]
        current = "port"
        key = "" ### wire name
        value = "" ### prot name
        for s in stat:
            if current == "port":
                value = s
                current = "("
            elif current == "(":
                current = "wire"
            elif current == "wire":
                if s == ")":
                    io_wire_table[key]= value
                    key = value = ""
                    current = "port"
                else:
                    key += s
            else:
                assert False
        return io_wire_table
    def get_wire_table_csv(self):
        from constructor_funcs import remove_signal_range
        csv_ = []
        
        ### top.input_port --> submodule.input_port
        for input_port in self.ls_input_port:
            for inst in self.dict_instance.keys():
                module_name = self.dict_instance[inst] 
                port = self.dict_wire_table[inst]["in"].get(input_port,"NotFound")
                if  port != "NotFound":
                    self.dict_wire_table[inst]["in"].pop(input_port)  ### checking no driven 
                    csv_.append(["input." + input_port, \
                                 "->", \
                                 "->" if "." + remove_signal_range(input_port) == port else input_port, \
                                 inst + ":" + module_name +  port])
        
        for inst in self.dict_instance.keys():
            module_name = self.dict_instance[inst] 
            for output in self.dict_wire_table[inst]["out"].keys():
                port = self.dict_wire_table[inst]["out"][output]
                ### submodule.output_port -> top.output_port
                if  self.ls_output_port.count(output) > 0:
                    self.ls_output_port.remove(output) ### checking no driven 
                    csv_.append([inst+ ":" + module_name + port, \
                                 "->" if "." + remove_signal_range(output) == port else output, \
                                 "->", \
                                 "output." + output])
                ### submodule.output_port -> submodule.input_port
                for inst_other in [i for i in self.dict_instance.keys() if i != inst]:
                    module_name_other = self.dict_instance[inst_other] 
                    port_other = self.dict_wire_table[inst_other]["in"].get(output,"NotFound")
                    if port_other != "NotFound":
                        self.dict_wire_table[inst_other]["in"].pop(output)### checking no driven 
                        csv_.append([inst+ ":" + module_name + port, \
                                     "->" if "." + remove_signal_range(output) == port else output, \
                                     "->" if "." + remove_signal_range(output) == port_other else output, \
                                     inst_other + ":" + module_name_other + port_other])
                            
        for inst in self.dict_instance.keys():
            if len(self.dict_wire_table[inst]["in"].values()) > 0:
                import sys
                print >> sys.stderr,  "===> not driven @" + inst + "<==="
                for o in self.dict_wire_table[inst]["in"].values():
                    print >> sys.stderr,  o
        csv_ = sorted(csv_, key=itemgetter(0, 3, 1, 2))
        return csv_
