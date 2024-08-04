VALUE = 1

import math
import pathlib as p
import sys
from types import ModuleType
from typing import Self

import inflect

__package__ = 'One'.lower()

eng = inflect.engine()

def int_to_filename(value: int) -> str:
  if value == 3.141592653589793:
    return 'pi.py'
  if value == 6.283185307179586:
    return 'tau.py'
  if value == 2.718281828459045:
    return 'e.py'
  for i in range(1, 100):
    sqrt = math.sqrt(i)
    if isinstance(sqrt, int):
      continue
    if len(str(sqrt)) < 8:
      continue
    if sqrt == value:
      return f'sqrt{i}.py'
  return f'{eng.number_to_words(value).replace('-', '_').replace(' ', '_').replace(',', '')}.py'.replace('minus', 'negative')

def filename_to_classname(filename: str) -> str:
  return filename.replace('.py', '').replace('_', ' ').title().replace(' ', '')

class One(ModuleType):
  def __new__(cls: ModuleType, _VALUE: int = None) -> Self:
    is_root = _VALUE is None

    if _VALUE is None:
      _VALUE = VALUE


    name = str(int_to_filename(_VALUE))
    doc = str(eng.number_to_words(_VALUE))
    self = ModuleType.__new__(cls, name, doc)
    self.name = name
    self.doc = doc
    self.value = _VALUE
    self._one_addable = True

    path = p.Path(name)
    thisfilepath = p.Path(__file__)
    if not path.is_dir() and thisfilepath != path:
      text = thisfilepath.read_text(encoding='utf-8').split('\n')
      text[0] = f"VALUE = {_VALUE!r}"

      text = '\n'.join(text)

      my_classname = One.__name__
      text = text.replace(my_classname, filename_to_classname(name))

      path.write_text(text, encoding='utf-8')

    if is_root:
      return self
    else:
      return __import__(name.removesuffix('.py'))

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(self.name, self.doc)

  def get_actual_value(self, other: Self | int | float) -> int | float | None:
    if isinstance(other, int | float):
      return other
    elif isinstance(other, ModuleType) and hasattr(other, '_one_addable') and other._one_addable:
      return other.value
    else:
      return None

  def __add__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for +: {type(self)!r} and {type(other)!r}')
    return One(self.value + val)

  def __radd__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for +: {type(other)!r} and {type(self)!r}')
    return One(val + self.value)

  def __sub__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for -: {type(self)!r} and {type(other)!r}')
    return One(self.value - val)

  def __rsub__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for -: {type(other)!r} and {type(self)!r}')
    return One(val - self.value)

  def __mul__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for *: {type(self)!r} and {type(other)!r}')
    return One(self.value * val)

  def __rmul__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for *: {type(other)!r} and {type(self)!r}')
    return One(val * self.value)

  def __truediv__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for /: {type(self)!r} and {type(other)!r}')
    return One(self.value / val)

  def __rtruediv__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for /: {type(other)!r} and {type(self)!r}')
    return One(val / self.value)

  def __floordiv__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for //: {type(self)!r} and {type(other)!r}')
    return One(self.value // val)

  def __rfloordiv__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for //: {type(other)!r} and {type(self)!r}')
    return One(val // self.value)

  def __mod__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for %: {type(self)!r} and {type(other)!r}')
    return One(self.value % val)

  def __rmod__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for %: {type(other)!r} and {type(self)!r}')
    return One(val % self.value)

  def __pow__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for **: {type(self)!r} and {type(other)!r}')
    return One(self.value ** val)

  def __rpow__(self: Self, other: Self) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f'unsupported operand type(s) for **: {type(other)!r} and {type(self)!r}')
    return One(val ** self.value)

  def __neg__(self: Self) -> Self:
    return One(-self.value)

  def __pos__(self: Self) -> Self:
    return One(+self.value)

  def __abs__(self: Self) -> Self:
    return One(abs(self.value))

  def __invert__(self: Self) -> Self:
    return One(~self.value)

  def __lt__(self: Self, other: Self | int | float) -> bool:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"TypeError: '<' not supported between instances of {type(self)!r} and {type(other)!r}")
    return self.value < val

  def __le__(self: Self, other: Self | int | float) -> bool:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"TypeError: '<=' not supported between instances of {type(self)!r} and {type(other)!r}")
    return self.value <= val

  def __eq__(self: Self, other: Self | int | float) -> bool:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"TypeError: '==' not supported between instances of {type(self)!r} and {type(other)!r}")
    return self.value == val

  def __ne__(self: Self, other: Self | int | float) -> bool:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"TypeError: '!=' not supported between instances of {type(self)!r} and {type(other)!r}")
    return self.value != val

  def __gt__(self: Self, other: Self | int | float) -> bool:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"TypeError: '>' not supported between instances of {type(self)!r} and {type(other)!r}")
    return self.value > val

  def __ge__(self: Self, other: Self | int | float) -> bool:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"TypeError: '>=' not supported between instances of {type(self)!r} and {type(other)!r}")
    return self.value >= val

  def __lshift__(self: Self, other: Self | int | float) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"unsupported operand type(s) for <<: {type(self)!r} and {type(other)!r}")
    return One(self.value << val)

  def __rshift__(self: Self, other: Self | int | float) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"unsupported operand type(s) for >>: {type(self)!r} and {type(other)!r}")
    return One(self.value >> val)

  def __rlshift__(self: Self, other: Self | int | float) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"unsupported operand type(s) for <<: {type(self)!r} and {type(other)!r}")
    return One(val << self.value)

  def __rrshift__(self: Self, other: Self | int | float) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"unsupported operand type(s) for >>: {type(self)!r} and {type(other)!r}")
    return One(val >> self.value)

  def __and__(self: Self, other: Self | int | float) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"unsupported operand type(s) for &: {type(self)!r} and {type(other)!r}")
    return One(self.value & val)

  def __rand__(self: Self, other: Self | int | float) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"unsupported operand type(s) for &: {type(self)!r} and {type(other)!r}")
    return One(val & self.value)

  def __xor__(self: Self, other: Self | int | float) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"unsupported operand type(s) for ^: {type(self)!r} and {type(other)!r}")
    return One(self.value ^ val)

  def __rxor__(self: Self, other: Self | int | float) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"unsupported operand type(s) for ^: {type(self)!r} and {type(other)!r}")
    return One(val ^ self.value)

  def __or__(self: Self, other: Self | int | float) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"unsupported operand type(s) for |: {type(self)!r} and {type(other)!r}")
    return One(self.value | val)

  def __ror__(self: Self, other: Self | int | float) -> Self:
    if (val := self.get_actual_value(other)) is None:
      raise TypeError(f"unsupported operand type(s) for |: {type(self)!r} and {type(other)!r}")
    return One(val | self.value)

  def __int__(self: Self) -> int:
    return int(self.value)

  def __float__(self: Self) -> float:
    return float(self.value)

this = One()

if __name__ == '__main__':
  print(this)
else:
  sys.modules[__name__] = this
