# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 02:29:39 2018

@author: ryotakata
"""

class Wire(object):
    def __init__(self, level_, name_, range_):
        self.level = level_
        self.type = ""
        self.name = name_
        self.range = range_
        return
        

class Input_port(Wire):
    def __init__(self, level_, name_, range_):
        super(Input_port, self).__init__(level_, name_, range_)
        self.type = "input"
        self.is_used = False
        self.is_drived = False
        return
    def get_str(self):
        str_ = self.level + "(I)" + self.name + self.range
        return str_
        
class Output_port(Wire):
    def __init__(self, level_, name_, range_):
        super(Output_port, self).__init__(level_, name_, range_)
        self.type = "output"
        self.is_used = False
        self.is_drived = False
        return
    def get_str(self):
        str_ = self.level + "(O)" + self.name + self.range
        return str_
        
class Local_wire(Wire):
    def __init__(self, level_, name_, range_):
        super(Local_wire, self).__init__(level_, name_, range_)
        self.type = "local"
        self.is_used = False
        self.is_drived = False
        return
    def get_str(self):
        str_ = self.level + "(L)" + self.name + self.range
        return str_
class Constant_(Wire):
    def __init__(self, level_, name_):
        super(Constant_, self).__init__(level_, name_,"")
        self.type = "constant"
        self.is_used = True
        return
    def get_str(self):
        str_ = self.level + "(C)" + self.name + self.range
        return str_
class Open_(Wire):
    def __init__(self, level_):
        super(Open_, self).__init__(level_, "open","")
        self.type = "open"
        self.is_drived = True
        return
    def get_str(self):
        str_ = self.level + "()" + self.name + self.range
        return str_