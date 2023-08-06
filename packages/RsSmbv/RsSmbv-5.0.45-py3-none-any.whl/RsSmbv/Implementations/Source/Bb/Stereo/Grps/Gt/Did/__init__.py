from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DidCls:
	"""Did commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("did", core, parent)

	@property
	def artHead(self):
		"""artHead commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_artHead'):
			from .ArtHead import ArtHeadCls
			self._artHead = ArtHeadCls(self._core, self._cmd_group)
		return self._artHead

	@property
	def compressed(self):
		"""compressed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_compressed'):
			from .Compressed import CompressedCls
			self._compressed = CompressedCls(self._core, self._cmd_group)
		return self._compressed

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dpty(self):
		"""dpty commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpty'):
			from .Dpty import DptyCls
			self._dpty = DptyCls(self._core, self._cmd_group)
		return self._dpty

	@property
	def stereo(self):
		"""stereo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stereo'):
			from .Stereo import StereoCls
			self._stereo = StereoCls(self._core, self._cmd_group)
		return self._stereo

	def clone(self) -> 'DidCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DidCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
