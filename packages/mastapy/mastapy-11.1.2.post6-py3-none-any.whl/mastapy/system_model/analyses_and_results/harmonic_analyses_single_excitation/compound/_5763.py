﻿'''_5763.py

StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2408
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5761, _5762, _5671
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5634
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation',)


class StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation(_5671.BevelGearSetCompoundHarmonicAnalysisOfSingleExcitation):
    '''StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2408.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2408.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2408.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2408.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def straight_bevel_gears_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5761.StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation]: 'StraightBevelGearsCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5761.StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def straight_bevel_meshes_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5762.StraightBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]: 'StraightBevelMeshesCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5762.StraightBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5634.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5634.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5634.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5634.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value
