from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SynchronizationCls:
	"""Synchronization commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("synchronization", core, parent)

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClocSyncMode:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CLOCk:SYNChronization:MODE \n
		Snippet: value: enums.ClocSyncMode = driver.source.bb.arbitrary.clock.synchronization.get_mode() \n
		Selects the synchronization mode. This parameter is used to enable generation of very precise synchronous signal of
		several connected R&S SGT. Note: If several instruments are connected, the connecting cables from the primary instrument
		to the secondary instrument one and between each two consecutive secondary instruments must have the same length and type.
		Avoid unnecessary cable length and branching points. \n
			:return: mode: NONE| PRIMary| SECondary| DIIN NONE The instrument is working in stand-alone mode. PRIMary The instrument provides all connected instrument with its synchronisation (including the trigger signal) and reference clock signal. SECondary The instrument receives the synchronisation and reference clock signal from another instrument working in primary mode. DIIN The instrument receives the synchronisation and reference clock signal from the 'DIG I/Q' connector.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CLOCk:SYNChronization:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClocSyncMode)

	def set_mode(self, mode: enums.ClocSyncMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CLOCk:SYNChronization:MODE \n
		Snippet: driver.source.bb.arbitrary.clock.synchronization.set_mode(mode = enums.ClocSyncMode.DIIN) \n
		Selects the synchronization mode. This parameter is used to enable generation of very precise synchronous signal of
		several connected R&S SGT. Note: If several instruments are connected, the connecting cables from the primary instrument
		to the secondary instrument one and between each two consecutive secondary instruments must have the same length and type.
		Avoid unnecessary cable length and branching points. \n
			:param mode: NONE| PRIMary| SECondary| DIIN NONE The instrument is working in stand-alone mode. PRIMary The instrument provides all connected instrument with its synchronisation (including the trigger signal) and reference clock signal. SECondary The instrument receives the synchronisation and reference clock signal from another instrument working in primary mode. DIIN The instrument receives the synchronisation and reference clock signal from the 'DIG I/Q' connector.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClocSyncMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CLOCk:SYNChronization:MODE {param}')

	def clone(self) -> 'SynchronizationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SynchronizationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
