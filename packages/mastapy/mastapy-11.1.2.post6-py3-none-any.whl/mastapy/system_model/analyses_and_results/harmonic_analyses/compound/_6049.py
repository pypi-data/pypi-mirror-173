﻿'''_6049.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2401
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _6047, _6048, _6043
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5881
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis(_6043.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2401.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2401.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2401.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2401.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_harmonic_analysis(self) -> 'List[_6047.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundHarmonicAnalysis, constructor.new(_6047.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_harmonic_analysis(self) -> 'List[_6048.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundHarmonicAnalysis, constructor.new(_6048.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5881.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5881.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5881.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5881.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis))
        return value
