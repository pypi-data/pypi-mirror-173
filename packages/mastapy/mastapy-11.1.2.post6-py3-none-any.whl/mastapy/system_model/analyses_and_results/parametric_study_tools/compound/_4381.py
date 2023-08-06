﻿'''_4381.py

PowerLoadCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2333
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6772
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4252
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4416
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'PowerLoadCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundParametricStudyTool',)


class PowerLoadCompoundParametricStudyTool(_4416.VirtualComponentCompoundParametricStudyTool):
    '''PowerLoadCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2333.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2333.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def load_cases(self) -> 'List[_6772.PowerLoadLoadCase]':
        '''List[PowerLoadLoadCase]: 'LoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCases, constructor.new(_6772.PowerLoadLoadCase))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_4252.PowerLoadParametricStudyTool]':
        '''List[PowerLoadParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4252.PowerLoadParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4252.PowerLoadParametricStudyTool]':
        '''List[PowerLoadParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4252.PowerLoadParametricStudyTool))
        return value
