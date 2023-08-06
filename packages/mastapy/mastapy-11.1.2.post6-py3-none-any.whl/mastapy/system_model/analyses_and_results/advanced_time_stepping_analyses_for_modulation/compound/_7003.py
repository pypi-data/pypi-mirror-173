﻿'''_7003.py

ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2382
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _7001, _7002, _7032
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6873
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation',)


class ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation(_7032.GearSetCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2382.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2382.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2382.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2382.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def concept_gears_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_7001.ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ConceptGearsCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_7001.ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_meshes_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_7002.ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ConceptMeshesCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_7002.ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6873.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6873.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6873.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6873.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
