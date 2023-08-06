﻿'''_4356.py

HypoidGearCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2394
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4217
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4298
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'HypoidGearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearCompoundParametricStudyTool',)


class HypoidGearCompoundParametricStudyTool(_4298.AGMAGleasonConicalGearCompoundParametricStudyTool):
    '''HypoidGearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2394.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2394.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4217.HypoidGearParametricStudyTool]':
        '''List[HypoidGearParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4217.HypoidGearParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4217.HypoidGearParametricStudyTool]':
        '''List[HypoidGearParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4217.HypoidGearParametricStudyTool))
        return value
