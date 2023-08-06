﻿'''_3863.py

ConicalGearCompoundPowerFlow
'''


from typing import List

from mastapy.gears.rating.conical import _487
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3731
from mastapy.system_model.analyses_and_results.power_flows.compound import _3889
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConicalGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearCompoundPowerFlow',)


class ConicalGearCompoundPowerFlow(_3889.GearCompoundPowerFlow):
    '''ConicalGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_rating(self) -> '_487.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_487.ConicalGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def conical_gear_duty_cycle_rating(self) -> '_487.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'ConicalGearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_487.ConicalGearDutyCycleRating)(self.wrapped.ConicalGearDutyCycleRating) if self.wrapped.ConicalGearDutyCycleRating else None

    @property
    def component_analysis_cases(self) -> 'List[_3731.ConicalGearPowerFlow]':
        '''List[ConicalGearPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3731.ConicalGearPowerFlow))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_3731.ConicalGearPowerFlow]':
        '''List[ConicalGearPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3731.ConicalGearPowerFlow))
        return value
