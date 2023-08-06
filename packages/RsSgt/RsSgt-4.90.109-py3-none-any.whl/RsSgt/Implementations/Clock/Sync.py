from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SyncCls:
	"""Sync commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sync", core, parent)

	def get_state(self) -> bool:
		"""SCPI: CLOCk:SYNC:[STATe] \n
		Snippet: value: bool = driver.clock.sync.get_state() \n
		Requires instruments working in secondary synchronization mode. Queries the status of the external clock source.
		The status indicates, if the external clock source of the secondary instrument is synchronized or not synchronized yet. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('CLOCk:SYNC:STATe?')
		return Conversions.str_to_bool(response)
