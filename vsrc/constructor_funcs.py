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

def trans_vsrc_to_ls2d(vsrc):
    """
    Verilogをstr型で読み込みparseした結果を2次元のstrリストで返す
    """
    ### //形式の1行コメントを削除
    vsrc = reptn(r"//.*\n").sub("\n", vsrc)
    ### /* */形式のコメントを削除
    vsrc = reptn(r"`timescale.*\n").sub("\n", vsrc)
    
    ### delete line of timescale
    vsrc = reptn(r"/\*[\s\S]*?\*/").sub("", vsrc)
    
    assert len(reptn(r"^module\s|\smodule\s").findall(vsrc)) == 1 and \
        len(reptn(r"\sendmodule\s").findall(vsrc)) == 1, \
        "m(-_-)m 1Fileに複数のmodule宣言があるVerilogには非対応. 1 File per Unit.\n" \
        + vsrc[0:100]

    ### begin end case endcaseの直後に;を付加
    vsrc = reptn(r"\sbegin\s").sub(" begin; ", vsrc)
    vsrc = reptn(r"\send\s").sub(" end; ", vsrc)
    vsrc = reptn(r"\scase\s").sub(" case; ", vsrc)
    vsrc = reptn(r"\sendcase\s").sub(" endcase; ", vsrc)
    vsrc = reptn(r"\sendmodule\s").sub(" endmodule; ", vsrc)
    
    ### 空行を削除
    vsrc = reptn(r"\n\s+\n").sub("\n", vsrc)
    ### 行末空白を削除
    vsrc = reptn(r"\s+\n").sub("\n", vsrc)
    vsrc = reptn(r"\s+").sub(" ",vsrc)

    ### \n改行を削除
    vsrc = reptn(r"\n").sub("", vsrc)
   
    ### ;でsplit
    vsrc = reptn(r";").split(vsrc)

    vsrc = [reptn(r"^\s+").sub("", x) for x in vsrc]
    vsrc = [reptn(r"\s+$").sub("", x) for x in vsrc]
    vsrc = [reptn(r"\s*,\s*").sub(" ", x) for x in vsrc]
    vsrc = [reptn(r"\s*:\s*").sub(" : ", x) for x in vsrc]
    vsrc = [reptn(r"\s*\(\s*").sub(" ( ", x) for x in vsrc]
    vsrc = [reptn(r"\s*\)\s*").sub(" ) ", x) for x in vsrc]
    vsrc = [reptn(r"\s*\[\s*").sub(" [ ", x) for x in vsrc]
    vsrc = [reptn(r"\s*\]\s*").sub(" ] ", x) for x in vsrc]

    ### 2次元リストに変換
    vsrc = [reptn(r"\s+").sub(" ",x) for x in vsrc]
    vsrc = [reptn(r"^\s+").sub("",x) for x in vsrc]
    vsrc = [reptn(r"\s+$").sub("",x) for x in vsrc]
    vsrc = [reptn(r"\s").split(x) for x in vsrc]
    return vsrc

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