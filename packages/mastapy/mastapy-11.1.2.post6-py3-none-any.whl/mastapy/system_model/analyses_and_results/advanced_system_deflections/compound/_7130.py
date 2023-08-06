﻿'''_7130.py

ConicalGearSetCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.gears.rating.conical import _495
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6997
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7156
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ConicalGearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearSetCompoundAdvancedSystemDeflection',)


class ConicalGearSetCompoundAdvancedSystemDeflection(_7156.GearSetCompoundAdvancedSystemDeflection):
    '''ConicalGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_rating(self) -> '_495.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_495.ConicalGearSetDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating is not None else None

    @property
    def conical_gear_duty_cycle_rating(self) -> '_495.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'ConicalGearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_495.ConicalGearSetDutyCycleRating)(self.wrapped.ConicalGearDutyCycleRating) if self.wrapped.ConicalGearDutyCycleRating is not None else None

    @property
    def assembly_analysis_cases(self) -> 'List[_6997.ConicalGearSetAdvancedSystemDeflection]':
        '''List[ConicalGearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6997.ConicalGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6997.ConicalGearSetAdvancedSystemDeflection]':
        '''List[ConicalGearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6997.ConicalGearSetAdvancedSystemDeflection))
        return value
