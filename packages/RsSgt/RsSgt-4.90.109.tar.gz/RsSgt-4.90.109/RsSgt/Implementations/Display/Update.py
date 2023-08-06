from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UpdateCls:
	"""Update commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("update", core, parent)

	def get_hold(self) -> bool:
		"""SCPI: DISPlay:UPDate:HOLD \n
		Snippet: value: bool = driver.display.update.get_hold() \n
		No command help available \n
			:return: hold: No help available
		"""
		response = self._core.io.query_str('DISPlay:UPDate:HOLD?')
		return Conversions.str_to_bool(response)

	def set_hold(self, hold: bool) -> None:
		"""SCPI: DISPlay:UPDate:HOLD \n
		Snippet: driver.display.update.set_hold(hold = False) \n
		No command help available \n
			:param hold: No help available
		"""
		param = Conversions.bool_to_str(hold)
		self._core.io.write(f'DISPlay:UPDate:HOLD {param}')
