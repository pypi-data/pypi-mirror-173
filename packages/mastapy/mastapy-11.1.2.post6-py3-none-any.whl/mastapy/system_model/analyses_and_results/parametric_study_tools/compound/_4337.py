﻿'''_4337.py

CycloidalAssemblyCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2428
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4190
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4392
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CycloidalAssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyCompoundParametricStudyTool',)


class CycloidalAssemblyCompoundParametricStudyTool(_4392.SpecialisedAssemblyCompoundParametricStudyTool):
    '''CycloidalAssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2428.CycloidalAssembly':
        '''CycloidalAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2428.CycloidalAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2428.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2428.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4190.CycloidalAssemblyParametricStudyTool]':
        '''List[CycloidalAssemblyParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4190.CycloidalAssemblyParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4190.CycloidalAssemblyParametricStudyTool]':
        '''List[CycloidalAssemblyParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4190.CycloidalAssemblyParametricStudyTool))
        return value
