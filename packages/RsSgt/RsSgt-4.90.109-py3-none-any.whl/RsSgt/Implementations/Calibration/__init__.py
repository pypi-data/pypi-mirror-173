from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CalibrationCls:
	"""Calibration commands group definition. 15 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calibration", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def bbin(self):
		"""bbin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbin'):
			from .Bbin import BbinCls
			self._bbin = BbinCls(self._core, self._cmd_group)
		return self._bbin

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def iqModulator(self):
		"""iqModulator commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_iqModulator'):
			from .IqModulator import IqModulatorCls
			self._iqModulator = IqModulatorCls(self._core, self._cmd_group)
		return self._iqModulator

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_level'):
			from .Level import LevelCls
			self._level = LevelCls(self._core, self._cmd_group)
		return self._level

	@property
	def roscillator(self):
		"""roscillator commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_roscillator'):
			from .Roscillator import RoscillatorCls
			self._roscillator = RoscillatorCls(self._core, self._cmd_group)
		return self._roscillator

	def clone(self) -> 'CalibrationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CalibrationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
