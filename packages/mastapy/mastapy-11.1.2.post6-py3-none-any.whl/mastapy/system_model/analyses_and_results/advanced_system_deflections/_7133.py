﻿'''_7133.py

ConceptGearAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2381
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6675
from mastapy.gears.rating.concept import _516
from mastapy.system_model.analyses_and_results.system_deflections import _2577
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7164
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ConceptGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearAdvancedSystemDeflection',)


class ConceptGearAdvancedSystemDeflection(_7164.GearAdvancedSystemDeflection):
    '''ConceptGearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2381.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2381.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6675.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6675.ConceptGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def component_detailed_analysis(self) -> '_516.ConceptGearRating':
        '''ConceptGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_516.ConceptGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2577.ConceptGearSystemDeflection]':
        '''List[ConceptGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2577.ConceptGearSystemDeflection))
        return value
