from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 523 total commands, 14 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	@property
	def awgn(self):
		"""awgn commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_awgn'):
			from .Awgn import AwgnCls
			self._awgn = AwgnCls(self._core, self._cmd_group)
		return self._awgn

	@property
	def bb(self):
		"""bb commands group. 8 Sub-classes, 4 commands."""
		if not hasattr(self, '_bb'):
			from .Bb import BbCls
			self._bb = BbCls(self._core, self._cmd_group)
		return self._bb

	@property
	def bbin(self):
		"""bbin commands group. 7 Sub-classes, 10 commands."""
		if not hasattr(self, '_bbin'):
			from .Bbin import BbinCls
			self._bbin = BbinCls(self._core, self._cmd_group)
		return self._bbin

	@property
	def correction(self):
		"""correction commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_correction'):
			from .Correction import CorrectionCls
			self._correction = CorrectionCls(self._core, self._cmd_group)
		return self._correction

	@property
	def frequency(self):
		"""frequency commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def inputPy(self):
		"""inputPy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def iq(self):
		"""iq commands group. 5 Sub-classes, 4 commands."""
		if not hasattr(self, '_iq'):
			from .Iq import IqCls
			self._iq = IqCls(self._core, self._cmd_group)
		return self._iq

	@property
	def loscillator(self):
		"""loscillator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_loscillator'):
			from .Loscillator import LoscillatorCls
			self._loscillator = LoscillatorCls(self._core, self._cmd_group)
		return self._loscillator

	@property
	def modulation(self):
		"""modulation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def path(self):
		"""path commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_path'):
			from .Path import PathCls
			self._path = PathCls(self._core, self._cmd_group)
		return self._path

	@property
	def phase(self):
		"""phase commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def power(self):
		"""power commands group. 6 Sub-classes, 5 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def pulm(self):
		"""pulm commands group. 2 Sub-classes, 7 commands."""
		if not hasattr(self, '_pulm'):
			from .Pulm import PulmCls
			self._pulm = PulmCls(self._core, self._cmd_group)
		return self._pulm

	@property
	def roscillator(self):
		"""roscillator commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_roscillator'):
			from .Roscillator import RoscillatorCls
			self._roscillator = RoscillatorCls(self._core, self._cmd_group)
		return self._roscillator

	def preset(self) -> None:
		"""SCPI: SOURce<HW>:PRESet \n
		Snippet: driver.source.preset() \n
			INTRO_CMD_HELP: Triggers an instrument reset. It has the same effect as: \n
			- The *RST command
			- The 'SGMA-GUI > Instrument Name > Preset' function. However, the command does not close open GUI dialogs like the function does. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SOURce<HW>:PRESet \n
		Snippet: driver.source.preset_with_opc() \n
			INTRO_CMD_HELP: Triggers an instrument reset. It has the same effect as: \n
			- The *RST command
			- The 'SGMA-GUI > Instrument Name > Preset' function. However, the command does not close open GUI dialogs like the function does. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSgt.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:PRESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_op_mode(self) -> enums.OpMode:
		"""SCPI: [SOURce<HW>]:OPMode \n
		Snippet: value: enums.OpMode = driver.source.get_op_mode() \n
		Sets the operation mode. \n
			:return: op_mode: NORMal| BBBYpass NORMal normal operation BBBYpass Baseband bypass mode
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:OPMode?')
		return Conversions.str_to_scalar_enum(response, enums.OpMode)

	def set_op_mode(self, op_mode: enums.OpMode) -> None:
		"""SCPI: [SOURce<HW>]:OPMode \n
		Snippet: driver.source.set_op_mode(op_mode = enums.OpMode.BBBYpass) \n
		Sets the operation mode. \n
			:param op_mode: NORMal| BBBYpass NORMal normal operation BBBYpass Baseband bypass mode
		"""
		param = Conversions.enum_scalar_to_str(op_mode, enums.OpMode)
		self._core.io.write(f'SOURce<HwInstance>:OPMode {param}')

	def clone(self) -> 'SourceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SourceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
