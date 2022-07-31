import json
from typing import Any

class Loco():
	def __init__(self, address:int) -> None:
		self.address = address
		self.direction = False
		self.speed = 0
		self.functions:list[LocoFunction] = [LocoFunction(i) for i in range(21)]

class LocoFunction:
	def __init__(self, index:int) -> None:
		self.index:int = index
		self.isOn:bool = False

	def setfunction(self) -> None:
		self.isOn = True

	def clearfuncrion(self) -> None:
		self.isOn = False

class LocoJSONEncode(json.JSONEncoder):
	def default(self, o: Any) -> Any:
		if isinstance(o, Loco):
			return {
				"address": o.address,
				"direction": o.direction,
				"speed": o.speed,
				"functions": [int(f.isOn) for f in o.functions]
				}
		return super().default(o)

"""
class LocoFunctionJSONEncode(json.JSONEncoder):
	def default(self, o: Any) -> Any:
		if isinstance(o, LocoFunction):
			return o.isOn
		return super().default(o)
"""