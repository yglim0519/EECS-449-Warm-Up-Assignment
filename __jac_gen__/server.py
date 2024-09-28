from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__

@_Jac.make_walker(on_entry=[_Jac.DSFunc('return_message', _Jac.RootType)], on_exit=[])
@__jac_dataclass__(eq=False)
class interact(_Jac.Walker):

    def return_message(self, _jac_here_: _Jac.RootType) -> None:
        _Jac.report({'response': 'Hello, world!'})

@_Jac.make_walker(on_entry=[_Jac.DSFunc('return_message', _Jac.RootType)], on_exit=[])
@__jac_dataclass__(eq=False)
class interact_with_body(_Jac.Walker):
    name: str

    def return_message(self, _jac_here_: _Jac.RootType) -> None:
        _Jac.report({'response': 'Hello, ' + self.name + '!'})

@_Jac.make_walker(on_entry=[_Jac.DSFunc('calculate', _Jac.RootType)], on_exit=[])
@__jac_dataclass__(eq=False)
class add_numbers(_Jac.Walker):
    num1: int
    num2: int

    def calculate(self, _jac_here_: _Jac.RootType) -> None:
        result = self.num1 + self.num2
        _Jac.report({'result': result, 'message': 'The sum of num1 and num2 is calculated successfully!'})

@_Jac.make_walker(on_entry=[_Jac.DSFunc('say_hello', _Jac.RootType)], on_exit=[])
@__jac_dataclass__(eq=False)
class greet_user(_Jac.Walker):
    name: str

    def say_hello(self, _jac_here_: _Jac.RootType) -> None:
        greeting = 'Hello, ' + self.name + '! Welcome!'
        _Jac.report({'greeting': greeting, 'message': 'User greeted successfully!'})