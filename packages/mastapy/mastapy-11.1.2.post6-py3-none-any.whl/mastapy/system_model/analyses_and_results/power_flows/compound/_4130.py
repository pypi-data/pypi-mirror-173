﻿'''_4130.py

StraightBevelSunGearCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.analyses_and_results.power_flows import _4000
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _4123
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'StraightBevelSunGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearCompoundPowerFlow',)


class StraightBevelSunGearCompoundPowerFlow(_4123.StraightBevelDiffGearCompoundPowerFlow):
    '''StraightBevelSunGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_4000.StraightBevelSunGearPowerFlow]':
        '''List[StraightBevelSunGearPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4000.StraightBevelSunGearPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4000.StraightBevelSunGearPowerFlow]':
        '''List[StraightBevelSunGearPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4000.StraightBevelSunGearPowerFlow))
        return value
