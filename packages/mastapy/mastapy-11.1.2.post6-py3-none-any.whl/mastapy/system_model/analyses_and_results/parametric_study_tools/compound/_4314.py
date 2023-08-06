﻿'''_4314.py

BoltedJointCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2305
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4166
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4392
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'BoltedJointCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundParametricStudyTool',)


class BoltedJointCompoundParametricStudyTool(_4392.SpecialisedAssemblyCompoundParametricStudyTool):
    '''BoltedJointCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2305.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2305.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2305.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2305.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4166.BoltedJointParametricStudyTool]':
        '''List[BoltedJointParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4166.BoltedJointParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4166.BoltedJointParametricStudyTool]':
        '''List[BoltedJointParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4166.BoltedJointParametricStudyTool))
        return value
