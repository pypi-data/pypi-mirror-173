﻿'''_5099.py

AGMAGleasonConicalGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses import _4946
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5127
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'AGMAGleasonConicalGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearSetCompoundModalAnalysis',)


class AGMAGleasonConicalGearSetCompoundModalAnalysis(_5127.ConicalGearSetCompoundModalAnalysis):
    '''AGMAGleasonConicalGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(self) -> 'List[_4946.AGMAGleasonConicalGearSetModalAnalysis]':
        '''List[AGMAGleasonConicalGearSetModalAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4946.AGMAGleasonConicalGearSetModalAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4946.AGMAGleasonConicalGearSetModalAnalysis]':
        '''List[AGMAGleasonConicalGearSetModalAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4946.AGMAGleasonConicalGearSetModalAnalysis))
        return value
