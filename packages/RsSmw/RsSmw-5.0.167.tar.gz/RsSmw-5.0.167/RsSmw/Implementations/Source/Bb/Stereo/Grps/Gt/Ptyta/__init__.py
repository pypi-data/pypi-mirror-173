from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PtytaCls:
	"""Ptyta commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ptyta", core, parent)

	@property
	def pty(self):
		"""pty commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pty'):
			from .Pty import PtyCls
			self._pty = PtyCls(self._core, self._cmd_group)
		return self._pty

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def ta(self):
		"""ta commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ta'):
			from .Ta import TaCls
			self._ta = TaCls(self._core, self._cmd_group)
		return self._ta

	def clone(self) -> 'PtytaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PtytaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
