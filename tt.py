#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tt

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      tt,v 1.0 2018年8月21日
    FROM:   2018年8月21日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

class Ttt(object):
    _t = None
    __pre = None
      
    @property
    @staticmethod
    def pre(cls):        
        return cls.__pre
    
    @pre.setter
    @staticmethod
    def pre(cls,value):
        cls.__pre = value    
    
    @staticmethod
    def _driver():
        return Ttt.__pre
        
    @staticmethod
    def __driver():
        print(Ttt.__pre)
        
    @staticmethod
    def p_pre():
        print(Ttt.__pre)

class Yyy(Ttt):
    @classmethod
    def test(cls):
        Ttt._driver()
        
    @classmethod
    def test2(cls):
        cls.__driver()
  
class Foo:
    __NAME=None
    
    @property
    def name(self):
        return self.__NAME #obj.name访问的是self.__NAME(这也是真实值的存放位置)

    @name.setter
    def name(self,value):
        if not isinstance(value,str): #在设定值之前进行类型检查
            raise TypeError('%s must be str' %value)
        self.__NAME=value #通过类型检查后,将值value存放到真实的位置self.__NAME

    @name.deleter
    def name(self):
        raise TypeError('Can not delete')
     
if __name__ == "__main__":
    
    Ttt.pre = 2
    print(Ttt.pre)
    t.pp_pre()
    

