﻿'''_3776.py

ConceptCouplingCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2441
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3646
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3787
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ConceptCouplingCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingCompoundStabilityAnalysis',)


class ConceptCouplingCompoundStabilityAnalysis(_3787.CouplingCompoundStabilityAnalysis):
    '''ConceptCouplingCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2441.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2441.ConceptCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2441.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2441.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3646.ConceptCouplingStabilityAnalysis]':
        '''List[ConceptCouplingStabilityAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3646.ConceptCouplingStabilityAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3646.ConceptCouplingStabilityAnalysis]':
        '''List[ConceptCouplingStabilityAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3646.ConceptCouplingStabilityAnalysis))
        return value
