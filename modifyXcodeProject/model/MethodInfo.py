#coding=utf-8

class MethodInfo:

    def __init__(self):

        self.methodNameList = [] #方法名字列表
        self.methodReturnType = '' #方法返回类型
        self.methodIsPrivate = None #是否私有方法
        self.methodContent = '' #方法体内容
        self.methodNameCanChange = 1 #方法是否可以修改
