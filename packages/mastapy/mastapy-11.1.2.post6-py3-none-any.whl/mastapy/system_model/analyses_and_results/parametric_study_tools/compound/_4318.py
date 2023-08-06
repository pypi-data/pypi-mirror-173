﻿'''_4318.py

CoaxialConnectionCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _2131
from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets.cycloidal import _2197
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4171
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4391
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CoaxialConnectionCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionCompoundParametricStudyTool',)


class CoaxialConnectionCompoundParametricStudyTool(_4391.ShaftToMountableComponentConnectionCompoundParametricStudyTool):
    '''CoaxialConnectionCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2131.CoaxialConnection':
        '''CoaxialConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2131.CoaxialConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def connection_design(self) -> '_2131.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2131.CoaxialConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_4171.CoaxialConnectionParametricStudyTool]':
        '''List[CoaxialConnectionParametricStudyTool]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_4171.CoaxialConnectionParametricStudyTool))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_4171.CoaxialConnectionParametricStudyTool]':
        '''List[CoaxialConnectionParametricStudyTool]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_4171.CoaxialConnectionParametricStudyTool))
        return value
