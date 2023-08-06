from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RntiCls:
	"""Rnti commands group definition. 10 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rnti", core, parent)

	@property
	def cs(self):
		"""cs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cs'):
			from .Cs import CsCls
			self._cs = CsCls(self._core, self._cmd_group)
		return self._cs

	@property
	def mcsc(self):
		"""mcsc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcsc'):
			from .Mcsc import McscCls
			self._mcsc = McscCls(self._core, self._cmd_group)
		return self._mcsc

	@property
	def msgb(self):
		"""msgb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_msgb'):
			from .Msgb import MsgbCls
			self._msgb = MsgbCls(self._core, self._cmd_group)
		return self._msgb

	@property
	def ra(self):
		"""ra commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ra'):
			from .Ra import RaCls
			self._ra = RaCls(self._core, self._cmd_group)
		return self._ra

	@property
	def sfi(self):
		"""sfi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfi'):
			from .Sfi import SfiCls
			self._sfi = SfiCls(self._core, self._cmd_group)
		return self._sfi

	@property
	def sl(self):
		"""sl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sl'):
			from .Sl import SlCls
			self._sl = SlCls(self._core, self._cmd_group)
		return self._sl

	@property
	def slcs(self):
		"""slcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slcs'):
			from .Slcs import SlcsCls
			self._slcs = SlcsCls(self._core, self._cmd_group)
		return self._slcs

	@property
	def spcsi(self):
		"""spcsi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spcsi'):
			from .Spcsi import SpcsiCls
			self._spcsi = SpcsiCls(self._core, self._cmd_group)
		return self._spcsi

	@property
	def tc(self):
		"""tc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tc'):
			from .Tc import TcCls
			self._tc = TcCls(self._core, self._cmd_group)
		return self._tc

	@property
	def v(self):
		"""v commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_v'):
			from .V import VCls
			self._v = VCls(self._core, self._cmd_group)
		return self._v

	def clone(self) -> 'RntiCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RntiCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
