from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbCls:
	"""Bb commands group definition. 244 total commands, 8 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bb", core, parent)

	@property
	def arbitrary(self):
		"""arbitrary commands group. 9 Sub-classes, 2 commands."""
		if not hasattr(self, '_arbitrary'):
			from .Arbitrary import ArbitraryCls
			self._arbitrary = ArbitraryCls(self._core, self._cmd_group)
		return self._arbitrary

	@property
	def impairment(self):
		"""impairment commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_impairment'):
			from .Impairment import ImpairmentCls
			self._impairment = ImpairmentCls(self._core, self._cmd_group)
		return self._impairment

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Info import InfoCls
			self._info = InfoCls(self._core, self._cmd_group)
		return self._info

	@property
	def path(self):
		"""path commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_path'):
			from .Path import PathCls
			self._path = PathCls(self._core, self._cmd_group)
		return self._path

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def progress(self):
		"""progress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_progress'):
			from .Progress import ProgressCls
			self._progress = ProgressCls(self._core, self._cmd_group)
		return self._progress

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def xmRadio(self):
		"""xmRadio commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_xmRadio'):
			from .XmRadio import XmRadioCls
			self._xmRadio = XmRadioCls(self._core, self._cmd_group)
		return self._xmRadio

	def get_cfactor(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:CFACtor \n
		Snippet: value: float = driver.source.bb.get_cfactor() \n
		This command queries the crest factor of the baseband signal. \n
			:return: cfactor: float Range: 0 to 100, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:CFACtor?')
		return Conversions.str_to_float(response)

	def get_foffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:FOFFset \n
		Snippet: value: float = driver.source.bb.get_foffset() \n
		Sets the frequency offset for the baseband signal. The offset affects the signal on the baseband block output. It shifts
		the useful baseband signal in the center frequency. \n
			:return: foffset: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:FOFFset?')
		return Conversions.str_to_float(response)

	def set_foffset(self, foffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:FOFFset \n
		Snippet: driver.source.bb.set_foffset(foffset = 1.0) \n
		Sets the frequency offset for the baseband signal. The offset affects the signal on the baseband block output. It shifts
		the useful baseband signal in the center frequency. \n
			:param foffset: float
		"""
		param = Conversions.decimal_value_to_str(foffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:FOFFset {param}')

	def get_pgain(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PGAin \n
		Snippet: value: float = driver.source.bb.get_pgain() \n
		The command sets the relative path gain for the selected baseband signal compared to the baseband signals of the other
		baseband sources (external baseband) . The gain affects the signal on the 'baseband block' output. \n
			:return: pgain: float Range: -50 to 50
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PGAin?')
		return Conversions.str_to_float(response)

	def set_pgain(self, pgain: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:PGAin \n
		Snippet: driver.source.bb.set_pgain(pgain = 1.0) \n
		The command sets the relative path gain for the selected baseband signal compared to the baseband signals of the other
		baseband sources (external baseband) . The gain affects the signal on the 'baseband block' output. \n
			:param pgain: float Range: -50 to 50
		"""
		param = Conversions.decimal_value_to_str(pgain)
		self._core.io.write(f'SOURce<HwInstance>:BB:PGAin {param}')

	def get_poffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:POFFset \n
		Snippet: value: float = driver.source.bb.get_poffset() \n
		Sets the relative phase offset of the baseband signal. The phase offset affects the signal of the 'Baseband Block' output. \n
			:return: ph_offset: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:POFFset?')
		return Conversions.str_to_float(response)

	def set_poffset(self, ph_offset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:POFFset \n
		Snippet: driver.source.bb.set_poffset(ph_offset = 1.0) \n
		Sets the relative phase offset of the baseband signal. The phase offset affects the signal of the 'Baseband Block' output. \n
			:param ph_offset: float
		"""
		param = Conversions.decimal_value_to_str(ph_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:POFFset {param}')

	def clone(self) -> 'BbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
