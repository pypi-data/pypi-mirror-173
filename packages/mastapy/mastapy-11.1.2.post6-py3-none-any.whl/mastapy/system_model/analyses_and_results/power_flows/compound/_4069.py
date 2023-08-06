﻿'''_4069.py

DatumCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2310
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3937
from mastapy.system_model.analyses_and_results.power_flows.compound import _4043
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'DatumCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundPowerFlow',)


class DatumCompoundPowerFlow(_4043.ComponentCompoundPowerFlow):
    '''DatumCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2310.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2310.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3937.DatumPowerFlow]':
        '''List[DatumPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3937.DatumPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3937.DatumPowerFlow]':
        '''List[DatumPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3937.DatumPowerFlow))
        return value
