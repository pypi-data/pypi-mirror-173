from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmrsCls:
	"""Dmrs commands group definition. 7 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmrs", core, parent)

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Length import LengthCls
			self._length = LengthCls(self._core, self._cmd_group)
		return self._length

	@property
	def nsid(self):
		"""nsid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsid'):
			from .Nsid import NsidCls
			self._nsid = NsidCls(self._core, self._cmd_group)
		return self._nsid

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def seqGen(self):
		"""seqGen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seqGen'):
			from .SeqGen import SeqGenCls
			self._seqGen = SeqGenCls(self._core, self._cmd_group)
		return self._seqGen

	@property
	def seqHopping(self):
		"""seqHopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seqHopping'):
			from .SeqHopping import SeqHoppingCls
			self._seqHopping = SeqHoppingCls(self._core, self._cmd_group)
		return self._seqHopping

	@property
	def sltSymbols(self):
		"""sltSymbols commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sltSymbols'):
			from .SltSymbols import SltSymbolsCls
			self._sltSymbols = SltSymbolsCls(self._core, self._cmd_group)
		return self._sltSymbols

	@property
	def apSelect(self):
		"""apSelect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apSelect'):
			from .ApSelect import ApSelectCls
			self._apSelect = ApSelectCls(self._core, self._cmd_group)
		return self._apSelect

	def clone(self) -> 'DmrsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DmrsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
