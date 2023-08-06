﻿'''_6103.py

ZerolBevelGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2414
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _6101, _6102, _5993
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5939
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'ZerolBevelGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundHarmonicAnalysis',)


class ZerolBevelGearSetCompoundHarmonicAnalysis(_5993.BevelGearSetCompoundHarmonicAnalysis):
    '''ZerolBevelGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2414.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2414.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2414.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2414.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def zerol_bevel_gears_compound_harmonic_analysis(self) -> 'List[_6101.ZerolBevelGearCompoundHarmonicAnalysis]':
        '''List[ZerolBevelGearCompoundHarmonicAnalysis]: 'ZerolBevelGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundHarmonicAnalysis, constructor.new(_6101.ZerolBevelGearCompoundHarmonicAnalysis))
        return value

    @property
    def zerol_bevel_meshes_compound_harmonic_analysis(self) -> 'List[_6102.ZerolBevelGearMeshCompoundHarmonicAnalysis]':
        '''List[ZerolBevelGearMeshCompoundHarmonicAnalysis]: 'ZerolBevelMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundHarmonicAnalysis, constructor.new(_6102.ZerolBevelGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5939.ZerolBevelGearSetHarmonicAnalysis]':
        '''List[ZerolBevelGearSetHarmonicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5939.ZerolBevelGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5939.ZerolBevelGearSetHarmonicAnalysis]':
        '''List[ZerolBevelGearSetHarmonicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5939.ZerolBevelGearSetHarmonicAnalysis))
        return value
