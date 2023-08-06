﻿'''_5124.py

ConceptGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2382
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5122, _5123, _5153
from mastapy.system_model.analyses_and_results.modal_analyses import _4971
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ConceptGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundModalAnalysis',)


class ConceptGearSetCompoundModalAnalysis(_5153.GearSetCompoundModalAnalysis):
    '''ConceptGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundModalAnalysis.TYPE'):
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
    def concept_gears_compound_modal_analysis(self) -> 'List[_5122.ConceptGearCompoundModalAnalysis]':
        '''List[ConceptGearCompoundModalAnalysis]: 'ConceptGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundModalAnalysis, constructor.new(_5122.ConceptGearCompoundModalAnalysis))
        return value

    @property
    def concept_meshes_compound_modal_analysis(self) -> 'List[_5123.ConceptGearMeshCompoundModalAnalysis]':
        '''List[ConceptGearMeshCompoundModalAnalysis]: 'ConceptMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundModalAnalysis, constructor.new(_5123.ConceptGearMeshCompoundModalAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4971.ConceptGearSetModalAnalysis]':
        '''List[ConceptGearSetModalAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4971.ConceptGearSetModalAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4971.ConceptGearSetModalAnalysis]':
        '''List[ConceptGearSetModalAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4971.ConceptGearSetModalAnalysis))
        return value
