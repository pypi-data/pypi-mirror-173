from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CellCls:
	"""Cell commands group definition. 129 total commands, 24 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cell", core, parent)
		
		self._cmd_group.multi_repcap_types = "CellNull,Cell"

	@property
	def afState(self):
		"""afState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_afState'):
			from .AfState import AfStateCls
			self._afState = AfStateCls(self._core, self._cmd_group)
		return self._afState

	@property
	def cardeply(self):
		"""cardeply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cardeply'):
			from .Cardeply import CardeplyCls
			self._cardeply = CardeplyCls(self._core, self._cmd_group)
		return self._cardeply

	@property
	def cbw(self):
		"""cbw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbw'):
			from .Cbw import CbwCls
			self._cbw = CbwCls(self._core, self._cmd_group)
		return self._cbw

	@property
	def cellId(self):
		"""cellId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cellId'):
			from .CellId import CellIdCls
			self._cellId = CellIdCls(self._core, self._cmd_group)
		return self._cellId

	@property
	def cif(self):
		"""cif commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cif'):
			from .Cif import CifCls
			self._cif = CifCls(self._core, self._cmd_group)
		return self._cif

	@property
	def cifPresent(self):
		"""cifPresent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cifPresent'):
			from .CifPresent import CifPresentCls
			self._cifPresent = CifPresentCls(self._core, self._cmd_group)
		return self._cifPresent

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Dfreq import DfreqCls
			self._dfreq = DfreqCls(self._core, self._cmd_group)
		return self._dfreq

	@property
	def dumRes(self):
		"""dumRes commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_dumRes'):
			from .DumRes import DumResCls
			self._dumRes = DumResCls(self._core, self._cmd_group)
		return self._dumRes

	@property
	def lte(self):
		"""lte commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_lte'):
			from .Lte import LteCls
			self._lte = LteCls(self._core, self._cmd_group)
		return self._lte

	@property
	def mapped(self):
		"""mapped commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mapped'):
			from .Mapped import MappedCls
			self._mapped = MappedCls(self._core, self._cmd_group)
		return self._mapped

	@property
	def n1Id(self):
		"""n1Id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n1Id'):
			from .N1Id import N1IdCls
			self._n1Id = N1IdCls(self._core, self._cmd_group)
		return self._n1Id

	@property
	def n2Id(self):
		"""n2Id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n2Id'):
			from .N2Id import N2IdCls
			self._n2Id = N2IdCls(self._core, self._cmd_group)
		return self._n2Id

	@property
	def nsspbch(self):
		"""nsspbch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsspbch'):
			from .Nsspbch import NsspbchCls
			self._nsspbch = NsspbchCls(self._core, self._cmd_group)
		return self._nsspbch

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	@property
	def pcFreq(self):
		"""pcFreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcFreq'):
			from .PcFreq import PcFreqCls
			self._pcFreq = PcFreqCls(self._core, self._cmd_group)
		return self._pcFreq

	@property
	def prs(self):
		"""prs commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_prs'):
			from .Prs import PrsCls
			self._prs = PrsCls(self._core, self._cmd_group)
		return self._prs

	@property
	def rpow(self):
		"""rpow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpow'):
			from .Rpow import RpowCls
			self._rpow = RpowCls(self._core, self._cmd_group)
		return self._rpow

	@property
	def schby(self):
		"""schby commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_schby'):
			from .Schby import SchbyCls
			self._schby = SchbyCls(self._core, self._cmd_group)
		return self._schby

	@property
	def shSpec(self):
		"""shSpec commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shSpec'):
			from .ShSpec import ShSpecCls
			self._shSpec = ShSpecCls(self._core, self._cmd_group)
		return self._shSpec

	@property
	def sspbch(self):
		"""sspbch commands group. 16 Sub-classes, 0 commands."""
		if not hasattr(self, '_sspbch'):
			from .Sspbch import SspbchCls
			self._sspbch = SspbchCls(self._core, self._cmd_group)
		return self._sspbch

	@property
	def syInfo(self):
		"""syInfo commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_syInfo'):
			from .SyInfo import SyInfoCls
			self._syInfo = SyInfoCls(self._core, self._cmd_group)
		return self._syInfo

	@property
	def tapos(self):
		"""tapos commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tapos'):
			from .Tapos import TaposCls
			self._tapos = TaposCls(self._core, self._cmd_group)
		return self._tapos

	@property
	def tmph(self):
		"""tmph commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_tmph'):
			from .Tmph import TmphCls
			self._tmph = TmphCls(self._core, self._cmd_group)
		return self._tmph

	@property
	def txbw(self):
		"""txbw commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_txbw'):
			from .Txbw import TxbwCls
			self._txbw = TxbwCls(self._core, self._cmd_group)
		return self._txbw

	def clone(self) -> 'CellCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CellCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
