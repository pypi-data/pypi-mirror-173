﻿'''_5214.py

UnbalancedMassCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2338
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _5068
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5215
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'UnbalancedMassCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundModalAnalysis',)


class UnbalancedMassCompoundModalAnalysis(_5215.VirtualComponentCompoundModalAnalysis):
    '''UnbalancedMassCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2338.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2338.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5068.UnbalancedMassModalAnalysis]':
        '''List[UnbalancedMassModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5068.UnbalancedMassModalAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5068.UnbalancedMassModalAnalysis]':
        '''List[UnbalancedMassModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5068.UnbalancedMassModalAnalysis))
        return value
