﻿'''_5561.py

FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2242
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5559, _5560, _5566
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5431
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation',)


class FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation(_5566.GearSetCompoundHarmonicAnalysisOfSingleExcitation):
    '''FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2242.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2242.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2242.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2242.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def face_gears_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5559.FaceGearCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearCompoundHarmonicAnalysisOfSingleExcitation]: 'FaceGearsCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5559.FaceGearCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def face_meshes_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5560.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation]: 'FaceMeshesCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5560.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5431.FaceGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5431.FaceGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5431.FaceGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5431.FaceGearSetHarmonicAnalysisOfSingleExcitation))
        return value
