from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuschCls:
	"""Pusch commands group definition. 6 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pusch", core, parent)

	@property
	def ccoding(self):
		"""ccoding commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Ccoding import CcodingCls
			self._ccoding = CcodingCls(self._core, self._cmd_group)
		return self._ccoding

	@property
	def naPort(self):
		"""naPort commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naPort'):
			from .NaPort import NaPortCls
			self._naPort = NaPortCls(self._core, self._cmd_group)
		return self._naPort

	def clone(self) -> 'PuschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PuschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
