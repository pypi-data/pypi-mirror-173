﻿'''_4321.py

ConceptCouplingConnectionCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2206
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4173
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4332
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ConceptCouplingConnectionCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionCompoundParametricStudyTool',)


class ConceptCouplingConnectionCompoundParametricStudyTool(_4332.CouplingConnectionCompoundParametricStudyTool):
    '''ConceptCouplingConnectionCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2206.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2206.ConceptCouplingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def connection_design(self) -> '_2206.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2206.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_4173.ConceptCouplingConnectionParametricStudyTool]':
        '''List[ConceptCouplingConnectionParametricStudyTool]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_4173.ConceptCouplingConnectionParametricStudyTool))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_4173.ConceptCouplingConnectionParametricStudyTool]':
        '''List[ConceptCouplingConnectionParametricStudyTool]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_4173.ConceptCouplingConnectionParametricStudyTool))
        return value
