#!/usr/bin/env python3




#
# class UserData:
#     sex="man"
#     def __init__(self,id,name):
#         self.id=id
#         self.name=name
#         self.__age=45
#
#     def test(self):
#         return "test"
#
#     @classmethod
#     def getname(cls):
#         return cls.
#
#     def __repr__(self):
#         return "ID:{id} Name:{name}".format(id=self.id,name=self.name)
#
# class NewUser(UserData):
#     def get_name(self):
#         return self.name
#     def set_name(self,value):
#         self.name=value
#
#
#
#     def __repr__(self):
#         return "{name}'s id is {id}".format(name=self.name,id=self.id)
#
# if _name__=="__main__":
#     # user1=NewUser(101,'jack')
#     # user1.set_name('jackie')
#     # user2=NewUser(102,'louplus')
#     # print(user1)
#     # print(user2)
#     # print(user1._UserData__age)
#     # print(user1.sex)
#     # print(UserData.sex)
#     print(UserData.getname())
#
# #
#
# class UserData:
#     def __init__(self,name):
#         self._name=name
class NewUser(object):

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        print(len(value))
        if len(value)<3:
            print("ERROR")
            # raise ValueError("err")
        else:
            self._name=value

if __name__=="__main__":
    user1=NewUser()
    user1.name="90234"
    user1.name="34"
    print user1.name



