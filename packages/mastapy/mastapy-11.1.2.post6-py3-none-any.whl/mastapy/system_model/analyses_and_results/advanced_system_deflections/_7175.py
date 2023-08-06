﻿'''_7175.py

KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2398
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6748
from mastapy.gears.rating.klingelnberg_hypoid import _380
from mastapy.system_model.analyses_and_results.system_deflections import _2628
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7172
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection',)


class KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection(_7172.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection):
    '''KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2398.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2398.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6748.KlingelnbergCycloPalloidHypoidGearLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6748.KlingelnbergCycloPalloidHypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def component_detailed_analysis(self) -> '_380.KlingelnbergCycloPalloidHypoidGearRating':
        '''KlingelnbergCycloPalloidHypoidGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_380.KlingelnbergCycloPalloidHypoidGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2628.KlingelnbergCycloPalloidHypoidGearSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2628.KlingelnbergCycloPalloidHypoidGearSystemDeflection))
        return value
