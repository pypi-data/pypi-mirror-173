﻿'''_2831.py

WormGearCompoundSystemDeflection
'''


from typing import List

from mastapy.gears.rating.worm import _343
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2411
from mastapy.system_model.analyses_and_results.system_deflections import _2693
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2765
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'WormGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundSystemDeflection',)


class WormGearCompoundSystemDeflection(_2765.GearCompoundSystemDeflection):
    '''WormGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_rating(self) -> '_343.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_343.WormGearDutyCycleRating)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating is not None else None

    @property
    def worm_duty_cycle_rating(self) -> '_343.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'WormDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_343.WormGearDutyCycleRating)(self.wrapped.WormDutyCycleRating) if self.wrapped.WormDutyCycleRating is not None else None

    @property
    def component_design(self) -> '_2411.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2411.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2693.WormGearSystemDeflection]':
        '''List[WormGearSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2693.WormGearSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2693.WormGearSystemDeflection]':
        '''List[WormGearSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2693.WormGearSystemDeflection))
        return value
