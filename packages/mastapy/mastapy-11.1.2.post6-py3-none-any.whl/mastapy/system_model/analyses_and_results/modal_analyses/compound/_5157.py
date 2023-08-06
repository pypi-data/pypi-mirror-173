﻿'''_5157.py

HypoidGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2395
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5155, _5156, _5099
from mastapy.system_model.analyses_and_results.modal_analyses import _5006
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'HypoidGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundModalAnalysis',)


class HypoidGearSetCompoundModalAnalysis(_5099.AGMAGleasonConicalGearSetCompoundModalAnalysis):
    '''HypoidGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2395.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2395.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2395.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2395.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def hypoid_gears_compound_modal_analysis(self) -> 'List[_5155.HypoidGearCompoundModalAnalysis]':
        '''List[HypoidGearCompoundModalAnalysis]: 'HypoidGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundModalAnalysis, constructor.new(_5155.HypoidGearCompoundModalAnalysis))
        return value

    @property
    def hypoid_meshes_compound_modal_analysis(self) -> 'List[_5156.HypoidGearMeshCompoundModalAnalysis]':
        '''List[HypoidGearMeshCompoundModalAnalysis]: 'HypoidMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundModalAnalysis, constructor.new(_5156.HypoidGearMeshCompoundModalAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5006.HypoidGearSetModalAnalysis]':
        '''List[HypoidGearSetModalAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5006.HypoidGearSetModalAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5006.HypoidGearSetModalAnalysis]':
        '''List[HypoidGearSetModalAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5006.HypoidGearSetModalAnalysis))
        return value
