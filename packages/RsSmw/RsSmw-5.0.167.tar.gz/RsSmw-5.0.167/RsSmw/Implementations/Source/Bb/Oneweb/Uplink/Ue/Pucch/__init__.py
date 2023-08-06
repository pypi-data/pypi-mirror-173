from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PucchCls:
	"""Pucch commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pucch", core, parent)

	@property
	def f1Naport(self):
		"""f1Naport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_f1Naport'):
			from .F1Naport import F1NaportCls
			self._f1Naport = F1NaportCls(self._core, self._cmd_group)
		return self._f1Naport

	@property
	def f2Naport(self):
		"""f2Naport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_f2Naport'):
			from .F2Naport import F2NaportCls
			self._f2Naport = F2NaportCls(self._core, self._cmd_group)
		return self._f2Naport

	@property
	def f3Naport(self):
		"""f3Naport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_f3Naport'):
			from .F3Naport import F3NaportCls
			self._f3Naport = F3NaportCls(self._core, self._cmd_group)
		return self._f3Naport

	def clone(self) -> 'PucchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PucchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
