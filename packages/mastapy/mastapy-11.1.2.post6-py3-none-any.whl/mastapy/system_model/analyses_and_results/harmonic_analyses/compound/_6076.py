﻿'''_6076.py

SpiralBevelGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2404
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _6074, _6075, _5993
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5911
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'SpiralBevelGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundHarmonicAnalysis',)


class SpiralBevelGearSetCompoundHarmonicAnalysis(_5993.BevelGearSetCompoundHarmonicAnalysis):
    '''SpiralBevelGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2404.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2404.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2404.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2404.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def spiral_bevel_gears_compound_harmonic_analysis(self) -> 'List[_6074.SpiralBevelGearCompoundHarmonicAnalysis]':
        '''List[SpiralBevelGearCompoundHarmonicAnalysis]: 'SpiralBevelGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundHarmonicAnalysis, constructor.new(_6074.SpiralBevelGearCompoundHarmonicAnalysis))
        return value

    @property
    def spiral_bevel_meshes_compound_harmonic_analysis(self) -> 'List[_6075.SpiralBevelGearMeshCompoundHarmonicAnalysis]':
        '''List[SpiralBevelGearMeshCompoundHarmonicAnalysis]: 'SpiralBevelMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundHarmonicAnalysis, constructor.new(_6075.SpiralBevelGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5911.SpiralBevelGearSetHarmonicAnalysis]':
        '''List[SpiralBevelGearSetHarmonicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5911.SpiralBevelGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5911.SpiralBevelGearSetHarmonicAnalysis]':
        '''List[SpiralBevelGearSetHarmonicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5911.SpiralBevelGearSetHarmonicAnalysis))
        return value
