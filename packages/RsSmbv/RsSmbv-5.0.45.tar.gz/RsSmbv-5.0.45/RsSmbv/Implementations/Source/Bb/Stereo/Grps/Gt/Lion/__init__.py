from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LionCls:
	"""Lion commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lion", core, parent)

	@property
	def eg(self):
		"""eg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eg'):
			from .Eg import EgCls
			self._eg = EgCls(self._core, self._cmd_group)
		return self._eg

	@property
	def ils(self):
		"""ils commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ils'):
			from .Ils import IlsCls
			self._ils = IlsCls(self._core, self._cmd_group)
		return self._ils

	@property
	def la(self):
		"""la commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_la'):
			from .La import LaCls
			self._la = LaCls(self._core, self._cmd_group)
		return self._la

	@property
	def lsn(self):
		"""lsn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lsn'):
			from .Lsn import LsnCls
			self._lsn = LsnCls(self._core, self._cmd_group)
		return self._lsn

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'LionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
