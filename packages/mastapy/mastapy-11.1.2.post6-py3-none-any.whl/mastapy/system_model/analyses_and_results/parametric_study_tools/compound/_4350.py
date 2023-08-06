﻿'''_4350.py

FEPartCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2314
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4210
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4296
from mastapy._internal.python_net import python_net_import

_FE_PART_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'FEPartCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCompoundParametricStudyTool',)


class FEPartCompoundParametricStudyTool(_4296.AbstractShaftOrHousingCompoundParametricStudyTool):
    '''FEPartCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _FE_PART_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2314.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2314.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4210.FEPartParametricStudyTool]':
        '''List[FEPartParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4210.FEPartParametricStudyTool))
        return value

    @property
    def planetaries(self) -> 'List[FEPartCompoundParametricStudyTool]':
        '''List[FEPartCompoundParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartCompoundParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4210.FEPartParametricStudyTool]':
        '''List[FEPartParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4210.FEPartParametricStudyTool))
        return value
