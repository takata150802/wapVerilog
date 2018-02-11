# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 22:52:57 2018

@author: ryotakata
"""
import sys
import csv

def get_str_from_path(path):
    str_ = "" 
    with open(path,"r") as fp:
        for line in fp:
            str_ += line
    return str_

def get_module_name_from_path(path_to_vsrc):
    from reptn_funcs import trans_vsrc_to_ls2d
    vsrc_txt = get_str_from_path(path_to_vsrc)
    return trans_vsrc_to_ls2d(vsrc_txt)[0][1]

class Vmodule:
    def __init__(self,path_to_vsrc, dict_path_to_vsrc_submodules, level_ = ""):
        from reptn_funcs import trans_vsrc_to_ls2d
        from constructor_funcs import init_ls_input_port
        from constructor_funcs import init_ls_output_port
        from constructor_funcs import init_ls_local_wire
        from constructor_funcs import init_dict_instance
        from constructor_funcs import init_dict_module
        self.level = level_
        vsrc_txt = get_str_from_path(path_to_vsrc)
        self.statement = trans_vsrc_to_ls2d(vsrc_txt)
        self.module_name = self.statement[0][1]
        self.ls_input_port = init_ls_input_port(self.statement, level_)
        self.ls_output_port = init_ls_output_port(self.statement, level_)
        self.ls_local_wire = init_ls_local_wire(self.statement, level_)
        self.dict_instance, self.dict_param, self.dict_statement = init_dict_instance(self.statement)
        self.dict_module = init_dict_module(self.dict_instance, dict_path_to_vsrc_submodules, level_)
        self.dict_port_wire_table = self.gen_dict_port_wire_table()
    def gen_dict_port_wire_table(self):
        dict_ = {}
        for i in self.dict_instance.keys():
            dict_[i] = self.gen_port_wire_table_at_instance(i)
        return dict_
        
    def gen_port_wire_table_at_instance(self,instance):
        from reptn_funcs import _parse_prot_wire_statement
        table_ = {}
        table_['in'] = []
        table_['out'] = []
        stat = self.dict_statement[instance]
        table_tmp = _parse_prot_wire_statement(stat)
        for port_wire in table_tmp:
            dict_ = {}
            port = wire = ""
            tmp = [w for w in self.ls_input_port if w.name == port_wire['wire']]
            tmp = self.__get_wire_from_list(port_wire['wire'], self.ls_input_port)
            if tmp == False:
                tmp = self.__get_wire_from_list(port_wire['wire'], self.ls_output_port)
            if tmp == False:
                tmp = self.__get_wire_from_list(port_wire['wire'], self.ls_local_wire)
            if tmp == False and port_wire['wire'] == "":
                from Wire import Open_
                tmp = Open_(self.level)
            import re
            if tmp == False and re.compile("(\d*'s*[dhobDHOB][abcdefABCDEF\d]+)|\d+").match(port_wire['wire']):
                from Wire import Constant_
                tmp = Constant_(self.level, port_wire['wire']) 
            wire = tmp
            
            tmp = [p for p in self.dict_module[instance].ls_input_port if p.name == port_wire['port']]
            if tmp != []:
                assert len(tmp) == 1
                port = tmp[0]
                dict_['port'] = port
                dict_['wire'] = wire
                table_['in'].append(dict_)
            tmp = [p for p in self.dict_module[instance].ls_output_port if p.name == port_wire['port']]
            if tmp != []:
                assert len(tmp) == 1
                port = tmp[0]
                dict_['port'] = port
                dict_['wire'] = wire
                table_['out'].append(dict_)
        return  table_
    
    def __get_wire_from_list(self,str_, ls_):
        import re
        if re.compile(r"\[.*\]").search(str_) != None:
            tmp = [w for w in ls_ if w.name + w.range == str_]
        else:
            tmp = [w for w in ls_ if re.compile(r"\[.*\]").sub("", w.name) == str_]
        if tmp != []:
            assert len(tmp) == 1
            return tmp[0]
        else:
            return False
    def get_assign_table(self):
        assign_table = []
        dict_ = {}
        for instance in self.dict_port_wire_table.keys():
            for port_wire in self.dict_port_wire_table[instance]['in']:
                p = port_wire["port"]
                w = port_wire["wire"]
                ## top.input -> submodule.input
                if w.type == "input":
                    p.is_drived = True
                    w.is_used = True
                    dict_["push"] = w
                    dict_["wire"] = w
                    dict_["pull"] = p
                    assign_table.append(dict_)
                    dict_ = {}
                    print w.level,w.name,w.range ,"->",p.level, p.name, p.range
                ## submodule.output -> submodule.input
                for instance_o in self.dict_port_wire_table.keys():
                    for port_wire_o in self.dict_port_wire_table[instance_o]['out']:
                        p_o = port_wire_o["port"]
                        w_o = port_wire_o["wire"]
                        if w == w_o:
                            p.is_drived = True
                            w.is_used = True
                            w_o.is_drived = True
                            p_o.is_used = True
                            dict_["push"] = p_o
                            dict_["wire"] = w
                            dict_["pull"] = p
                            assign_table.append(dict_)
                            dict_ = {}
                            print p_o.level, p_o.name, p_o.range, "->", w.level,w_o.name,w_o.range, "->", w.level,w.name,w.range ,"->",p.level, p.name, p.range

            ### submodule.output -> top.output
            for port_wire in self.dict_port_wire_table[instance]['out']:
                p = port_wire["port"]
                w = port_wire["wire"]
                if w.type == "output":
                    p.is_used = True
                    w.is_drived = True
                    dict_["push"] = p
                    dict_["wire"] = w
                    dict_["pull"] = w
                    assign_table.append(dict_)
                    dict_ = {}
                    print p.level, p.name, p.range, "->", w.level,w.name,w.range
            
                    
        ### checking not used or dirved
        for w in self.ls_input_port:
            if w.is_used == False:
                print >> sys.stderr, w.name, "is not used!"
        for w in self.ls_output_port:
            if w.is_drived == False:
                print >> sys.stderr, w.name, "is not drived!"
        for w in self.ls_local_wire:
            if w.is_used == False:
                print >> sys.stderr, w.name, "is not used!"
            if w.is_drived == False:
                print >> sys.stderr, w.name, "is not drived!"
        for i in self.dict_port_wire_table.keys():
            for port_wire in self.dict_port_wire_table[instance]['out']:
                if port_wire['port'].is_used == False:
                    print >> sys.stderr, port_wire['port'].level + "." + port_wire['port'].name, "is not used!"
            for port_wire in self.dict_port_wire_table[instance]['in']:
                if port_wire['port'].is_drived == False:
                    print >> sys.stderr, port_wire['port'].level + "." + port_wire['port'].name, "is not drived!"
        return assign_table
        
    def get_csv(self):
        for i in self.dict_module.keys():
            self.dict_module[i].get_csv()
        print  "====>", self.module_name
        self.get_assign_table()
        csv_ = []
        return csv_


if __name__ == '__main__':
    args = sys.argv
    dict_path_to_vsrc = {}
    for v in args[2:]:
        dict_path_to_vsrc[get_module_name_from_path(v)] = v
    path_to_vsrc_top = dict_path_to_vsrc.pop(args[1])
    top = Vmodule(path_to_vsrc_top, dict_path_to_vsrc)
    top.get_csv()