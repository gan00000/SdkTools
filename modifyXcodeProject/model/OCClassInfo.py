#coding=utf-8

class OCClassInfo:

    def __init__(self):

        self.propertyList = []  #类属性集合,对外，声明在.h
        self.priPropertyList = []
        self.methodList = []    #类方法集合
        self.name = ''  #类名
        self.protocolNameList = None  #实现的协议名称
        self.instMethodList = [] #返回实例的方法
        

