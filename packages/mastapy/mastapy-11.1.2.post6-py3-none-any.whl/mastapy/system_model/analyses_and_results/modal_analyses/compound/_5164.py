﻿'''_5164.py

KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2399
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5162, _5163, _5161
from mastapy.system_model.analyses_and_results.modal_analyses import _5013
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis(_5161.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2399.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2399.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2399.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2399.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_modal_analysis(self) -> 'List[_5162.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundModalAnalysis, constructor.new(_5162.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_modal_analysis(self) -> 'List[_5163.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundModalAnalysis, constructor.new(_5163.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5013.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5013.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5013.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5013.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis))
        return value
