from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SmodulationCls:
	"""Smodulation commands group definition. 5 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("smodulation", core, parent)

	@property
	def clock(self):
		"""clock commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def rcvState(self):
		"""rcvState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rcvState'):
			from .RcvState import RcvStateCls
			self._rcvState = RcvStateCls(self._core, self._cmd_group)
		return self._rcvState

	@property
	def throughput(self):
		"""throughput commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_throughput'):
			from .Throughput import ThroughputCls
			self._throughput = ThroughputCls(self._core, self._cmd_group)
		return self._throughput

	# noinspection PyTypeChecker
	def get_border(self) -> enums.BitOrder:
		"""SCPI: [SOURce<HW>]:BB:DM:SMODulation:BORDer \n
		Snippet: value: enums.BitOrder = driver.source.bb.dm.smodulation.get_border() \n
		No command help available \n
			:return: bit_order: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:SMODulation:BORDer?')
		return Conversions.str_to_scalar_enum(response, enums.BitOrder)

	def set_border(self, bit_order: enums.BitOrder) -> None:
		"""SCPI: [SOURce<HW>]:BB:DM:SMODulation:BORDer \n
		Snippet: driver.source.bb.dm.smodulation.set_border(bit_order = enums.BitOrder.LSBit) \n
		No command help available \n
			:param bit_order: No help available
		"""
		param = Conversions.enum_scalar_to_str(bit_order, enums.BitOrder)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:SMODulation:BORDer {param}')

	def get_cdt_deviation(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:DM:SMODulation:CDTDeviation \n
		Snippet: value: float = driver.source.bb.dm.smodulation.get_cdt_deviation() \n
		No command help available \n
			:return: deviation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:SMODulation:CDTDeviation?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'SmodulationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SmodulationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
