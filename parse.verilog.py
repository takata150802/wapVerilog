#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv
from vsrc.Vsrc import Vsrc


def argsparse(args):
    assert len(args) >= 1,\
    "m(-_-)m This script takes one argument.\
    \n usage: $python ./parse.verilog.py FJAICORE.v\
    \n args[1]: path to Verilog source."
    return args[1]
            
if __name__ == '__main__':
    """args[1]に指定したVerilogファイルから、
    args[2:]に指定した下位モジュールの全インスタンスの情報を取得し
    csv形式で出力するスクリプト.
    出力したcsvはcardとしてリピータモジュールのregmapの作成に使用する
    """
    args = sys.argv
    path_to_vsrc = argsparse(args)
    ### vsrc_txtにVerilogを文字列形式でload
    vsrc_txt = "" 
    with open(path_to_vsrc,"r") as fp:
        for line in fp:
            vsrc_txt += line
    vsrc = Vsrc(vsrc_txt)