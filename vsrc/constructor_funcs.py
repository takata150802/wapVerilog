# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 23:29:39 2018

@author: ryotakata
"""
import re
def reptn(str_):
    """
    pythonの正規表現文字列処理モジュールで
    strのパターンをコンパイルする
    """
    return re.compile(str_)


def init_ls_input_port(statement, level_ = ""):
    from Wire import Input_port
    ls_ = []
    for s in statement:
        if s[0]=="input":
            name_ = range_ = ""
            if s[1] == "[":
                i = 1
                while (s[i]!="]"):
                    i = i + 1
                range_ = reduce(lambda x, y : x + y, s[1:i+1])
                name_ = s[i+1]
            else:
                name_ = s[1]
            ls_.append(Input_port(level_, name_, range_))
    return ls_
def init_ls_output_port(statement, level_ = ""):
    from Wire import Output_port
    ls_ = []
    for s in statement:
        if s[0]=="output":
            name_ = range_ = ""
            if s[1] == "[":
                i = 1
                while (s[i]!="]"):
                    i = i + 1
                range_ = reduce(lambda x, y : x + y, s[1:i+1])
                name_ = s[i+1]
            else:
                name_ = s[1]
            ls_.append(Output_port(level_, name_, range_))
    return ls_
def init_ls_local_wire(statement, level_ = ""):
    from Wire import Local_wire
    ls_ = []
    for s in statement:
        if s[0]=="wire":
            name_ = range_ = ""
            if s[1] == "[":
                i = 1
                while (s[i]!="]"):
                    i = i + 1
                range_ = reduce(lambda x, y : x + y, s[1:i+1])
                name_ = s[i+1]
            else:
                name_ = s[1]
            ls_.append(Local_wire(level_, name_, range_))
    return ls_
def init_dict_instance(statement):
    from is_verilog_reserved_word import is_verilog_reserved_word
    dict_inst = {}
    dict_param = {}
    dict_statement = {}
    for s in statement:
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

def init_dict_module(dict_instance, dict_path_to_vsrc_submodules, level_ = ""):
    from Vmodule import Vmodule
    dict_module = {}
    for i in dict_instance.keys():
        m = dict_instance[i]
        path = dict_path_to_vsrc_submodules[m]
        level_arg = "" if level_ == "" else level_ + "."
        level_arg = level_arg + i + ":" + m
        dict_module[i] = Vmodule(path, dict_path_to_vsrc_submodules, level_arg)
    return dict_module
    

def is_input_port(vsrc, str_):
    ls_port = ["." + reptn(r"\[.*\]").sub("", i) for i in vsrc.ls_input_port]
    if len([s for s in [i for i in ls_port] if s == str_]) > 0:
        return True
    else:
        return False
def is_output_port(vsrc, str_):
    ls_port = ["." + reptn(r"\[.*\]").sub("", i) for i in vsrc.ls_output_port]
    if len([s for s in [i for i in ls_port] if s == str_]) > 0:
        return True
    else:
        return False

def remove_signal_range(str_):
    return reptn(r"\[.*\]").sub("", str_) 