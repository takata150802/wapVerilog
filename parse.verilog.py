#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv

from vsrc.Vmodule import Vmodule
from vsrc.Vmodule import get_module_name_from_path

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
    
    ### モジュールが重複宣言されていないかチェック
    assert are_there_duplication_1dlist( [get_module_name_from_path(v) for v in ls_path_to_vsrc]) == True,\
        "multiple definition of " "%s" % get_duplication_1dlist( [get_module_name_from_path(v) for v in ls_path_to_vsrc])
    ### top_module_nameに指定されたモジュールをインスタンス化
    dict_path_to_vsrc = {}
    for v in ls_path_to_vsrc:
        dict_path_to_vsrc[get_module_name_from_path(v)] = v
    path_to_vsrc_top = dict_path_to_vsrc.pop(top_module_name)
    top = Vmodule(path_to_vsrc_top, dict_path_to_vsrc)
    
    ### 階層を再帰的に辿って接続関係をcsvに出力
    csv_ = top.get_csv()
    with open(top_module_name + '_tabel.csv', 'w') as fp:
        writer = csv.writer(fp, lineterminator='\n')
        writer.writerows(csv_)
#    for l in csv_:
#        print l