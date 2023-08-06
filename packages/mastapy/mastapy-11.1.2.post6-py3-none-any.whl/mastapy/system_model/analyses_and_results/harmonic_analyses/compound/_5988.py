﻿'''_5988.py

BevelDifferentialGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2376
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5986, _5987, _5993
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5796
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'BevelDifferentialGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundHarmonicAnalysis',)


class BevelDifferentialGearSetCompoundHarmonicAnalysis(_5993.BevelGearSetCompoundHarmonicAnalysis):
    '''BevelDifferentialGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2376.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2376.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2376.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2376.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def bevel_differential_gears_compound_harmonic_analysis(self) -> 'List[_5986.BevelDifferentialGearCompoundHarmonicAnalysis]':
        '''List[BevelDifferentialGearCompoundHarmonicAnalysis]: 'BevelDifferentialGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundHarmonicAnalysis, constructor.new(_5986.BevelDifferentialGearCompoundHarmonicAnalysis))
        return value

    @property
    def bevel_differential_meshes_compound_harmonic_analysis(self) -> 'List[_5987.BevelDifferentialGearMeshCompoundHarmonicAnalysis]':
        '''List[BevelDifferentialGearMeshCompoundHarmonicAnalysis]: 'BevelDifferentialMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundHarmonicAnalysis, constructor.new(_5987.BevelDifferentialGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5796.BevelDifferentialGearSetHarmonicAnalysis]':
        '''List[BevelDifferentialGearSetHarmonicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5796.BevelDifferentialGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5796.BevelDifferentialGearSetHarmonicAnalysis]':
        '''List[BevelDifferentialGearSetHarmonicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5796.BevelDifferentialGearSetHarmonicAnalysis))
        return value
