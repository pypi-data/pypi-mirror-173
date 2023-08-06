﻿'''_4110.py

RollingRingCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2456
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3981
from mastapy.system_model.analyses_and_results.power_flows.compound import _4057
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'RollingRingCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundPowerFlow',)


class RollingRingCompoundPowerFlow(_4057.CouplingHalfCompoundPowerFlow):
    '''RollingRingCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2456.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2456.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3981.RollingRingPowerFlow]':
        '''List[RollingRingPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3981.RollingRingPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3981.RollingRingPowerFlow]':
        '''List[RollingRingPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3981.RollingRingPowerFlow))
        return value
