#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv
from vsrc.Vsrc import Vsrc
from vsrc.Vsrc import Wapvsrc


def argsparse(args):
    assert len(args) >= 3,\
    "m(-_-)m This script takes two or more arguments.\
    \n usage: $python ./parse.verilog.py top_module_name top_module_anme.v m0.v m1.v\
    \n args[2:]: path to Verilog source."
    return args[1], args[2:]
    
def are_there_duplication_1dlist(ls_):
    if len( [e for e in set(ls_) if ls_.count(e) > 1]) == 0:
        return True
    else:
        return False

def get_duplication_1dlist(ls_):
    return [e for e in set(ls_) if ls_.count(e) > 1]
        
            
if __name__ == '__main__':
    """
    """
    args = sys.argv
    top_module_name, ls_path_to_vsrc = argsparse(args)
    ls_vsrc = []
    for path_to_vsrc in ls_path_to_vsrc:
        vsrc_txt = "" 
        with open(path_to_vsrc,"r") as fp:
            for line in fp:
                vsrc_txt += line
        ls_vsrc.append(Vsrc(vsrc_txt))
            
    ### モジュールが重複宣言されていないかチェック
    assert are_there_duplication_1dlist( [v.module_name for v in ls_vsrc]) == True,\
        "multiple definition of " "%s" % get_duplication_1dlist( [v.module_name for v in ls_vsrc])
    
    ### topに指定されたモジュールを取得
    top_vsrc = [v for v in ls_vsrc if v.module_name == top_module_name][0]
    ls_vsrc.remove(top_vsrc)
    dict_vsrc = {}
    for v in ls_vsrc:
        dict_vsrc[v.module_name] = v
    top_vsrc = Wapvsrc(top_vsrc, dict_vsrc)

    for input_port in top_vsrc.ls_input_port:
        for inst in top_vsrc.dict_instance.keys():
            module_name = top_vsrc.dict_instance[inst] 
            port = top_vsrc.dict_wire_table[inst]["in"].get(input_port,"NotFound")
            if  port != "NotFound":
                print "input." + input_port + "," + input_port + "," + inst + ":" + module_name +  port  

    for inst in top_vsrc.dict_instance.keys():
        module_name = top_vsrc.dict_instance[inst] 
        for output in top_vsrc.dict_wire_table[inst]["out"].keys():
            port = top_vsrc.dict_wire_table[inst]["out"][output]
            if  top_vsrc.ls_output_port.count(output) > 0:
                print inst+ ":" + module_name + port + "," + output + "," + "output." + output
            for inst_other in [i for i in top_vsrc.dict_instance.keys() if i != inst]:
                module_name_other = top_vsrc.dict_instance[inst_other] 
                port_other = top_vsrc.dict_wire_table[inst_other]["in"].get(output,"NotFound")
                if port_other != "NotFound":
                    print inst+ ":" + module_name + port + "," + output + "," + \
                        inst_other + ":" + module_name_other + port_other
