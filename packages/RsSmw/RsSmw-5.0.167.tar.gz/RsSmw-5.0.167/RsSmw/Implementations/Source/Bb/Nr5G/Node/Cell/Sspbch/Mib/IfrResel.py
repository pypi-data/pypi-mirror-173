from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IfrReselCls:
	"""IfrResel commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ifrResel", core, parent)

	def set(self, ssp_bch_in_freq_sel: enums.FreqSel, cellNull=repcap.CellNull.Nr0, ssPbchNull=repcap.SsPbchNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH0>:SSPBch<ST0>:MIB:IFRResel \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.mib.ifrResel.set(ssp_bch_in_freq_sel = enums.FreqSel.ALWD, cellNull = repcap.CellNull.Nr0, ssPbchNull = repcap.SsPbchNull.Default) \n
		Sets the value of the system information parameter intraFreqReselection. \n
			:param ssp_bch_in_freq_sel: ALWD| NALW
			:param cellNull: optional repeated capability selector. Default value: Nr0
			:param ssPbchNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.enum_scalar_to_str(ssp_bch_in_freq_sel, enums.FreqSel)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		ssPbchNull_cmd_val = self._cmd_group.get_repcap_cmd_value(ssPbchNull, repcap.SsPbchNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{ssPbchNull_cmd_val}:MIB:IFRResel {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Nr0, ssPbchNull=repcap.SsPbchNull.Default) -> enums.FreqSel:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH0>:SSPBch<ST0>:MIB:IFRResel \n
		Snippet: value: enums.FreqSel = driver.source.bb.nr5G.node.cell.sspbch.mib.ifrResel.get(cellNull = repcap.CellNull.Nr0, ssPbchNull = repcap.SsPbchNull.Default) \n
		Sets the value of the system information parameter intraFreqReselection. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0
			:param ssPbchNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: ssp_bch_in_freq_sel: ALWD| NALW"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		ssPbchNull_cmd_val = self._cmd_group.get_repcap_cmd_value(ssPbchNull, repcap.SsPbchNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{ssPbchNull_cmd_val}:MIB:IFRResel?')
		return Conversions.str_to_scalar_enum(response, enums.FreqSel)
