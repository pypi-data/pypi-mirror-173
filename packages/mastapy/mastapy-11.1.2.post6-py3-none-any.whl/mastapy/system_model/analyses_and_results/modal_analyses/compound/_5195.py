﻿'''_5195.py

SpringDamperCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2460
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _5051
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5130
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'SpringDamperCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundModalAnalysis',)


class SpringDamperCompoundModalAnalysis(_5130.CouplingCompoundModalAnalysis):
    '''SpringDamperCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2460.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2460.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2460.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2460.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5051.SpringDamperModalAnalysis]':
        '''List[SpringDamperModalAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5051.SpringDamperModalAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5051.SpringDamperModalAnalysis]':
        '''List[SpringDamperModalAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5051.SpringDamperModalAnalysis))
        return value
