from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DexchangeCls:
	"""Dexchange commands group definition. 8 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dexchange", core, parent)

	@property
	def afile(self):
		"""afile commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_afile'):
			from .Afile import AfileCls
			self._afile = AfileCls(self._core, self._cmd_group)
		return self._afile

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.DexchMode:
		"""SCPI: [SOURce<HW>]:CORRection:DEXChange:MODE \n
		Snippet: value: enums.DexchMode = driver.source.correction.dexchange.get_mode() \n
		Selects if user correction lists should be imported or exported. Depending on the selection her, the file select command
		define either the source or the destination for user correction lists and ASCII files. \n
			:return: mode: IMPort| EXPort
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:DEXChange:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DexchMode)

	def set_mode(self, mode: enums.DexchMode) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:DEXChange:MODE \n
		Snippet: driver.source.correction.dexchange.set_mode(mode = enums.DexchMode.EXPort) \n
		Selects if user correction lists should be imported or exported. Depending on the selection her, the file select command
		define either the source or the destination for user correction lists and ASCII files. \n
			:param mode: IMPort| EXPort
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.DexchMode)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:DEXChange:MODE {param}')

	def get_select(self) -> str:
		"""SCPI: [SOURce<HW>]:CORRection:DEXChange:SELect \n
		Snippet: value: str = driver.source.correction.dexchange.get_select() \n
		Selects the user correction list to be imported or exported. The user correction files are stored with the fixed file
		extensions *.uco in a directory of the user's choice. The directory applicable to the commands is defined with the
		command method RsSgt.MassMemory.currentDirectory. A path can also be specified in command SOUR:CORR:DEXC:SEL, in which
		case the files are stored or loaded in the specified directory. \n
			:return: filename: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:DEXChange:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:DEXChange:SELect \n
		Snippet: driver.source.correction.dexchange.set_select(filename = '1') \n
		Selects the user correction list to be imported or exported. The user correction files are stored with the fixed file
		extensions *.uco in a directory of the user's choice. The directory applicable to the commands is defined with the
		command method RsSgt.MassMemory.currentDirectory. A path can also be specified in command SOUR:CORR:DEXC:SEL, in which
		case the files are stored or loaded in the specified directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:DEXChange:SELect {param}')

	def clone(self) -> 'DexchangeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DexchangeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
