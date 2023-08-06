﻿'''_5132.py

CouplingHalfCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses import _4979
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5170
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CouplingHalfCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundModalAnalysis',)


class CouplingHalfCompoundModalAnalysis(_5170.MountableComponentCompoundModalAnalysis):
    '''CouplingHalfCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_4979.CouplingHalfModalAnalysis]':
        '''List[CouplingHalfModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4979.CouplingHalfModalAnalysis))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_4979.CouplingHalfModalAnalysis]':
        '''List[CouplingHalfModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4979.CouplingHalfModalAnalysis))
        return value
