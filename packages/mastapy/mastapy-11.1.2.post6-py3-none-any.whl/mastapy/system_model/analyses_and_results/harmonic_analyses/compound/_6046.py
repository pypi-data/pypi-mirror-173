﻿'''_6046.py

KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2399
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _6044, _6045, _6043
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5878
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis(_6043.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis.TYPE'):
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
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_harmonic_analysis(self) -> 'List[_6044.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundHarmonicAnalysis, constructor.new(_6044.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_harmonic_analysis(self) -> 'List[_6045.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundHarmonicAnalysis, constructor.new(_6045.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5878.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5878.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5878.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5878.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis))
        return value
