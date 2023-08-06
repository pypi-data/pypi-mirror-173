﻿'''_4951.py

CycloidalDiscCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2246
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4799
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4907
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CycloidalDiscCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundModalAnalysis',)


class CycloidalDiscCompoundModalAnalysis(_4907.AbstractShaftCompoundModalAnalysis):
    '''CycloidalDiscCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2246.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2246.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4799.CycloidalDiscModalAnalysis]':
        '''List[CycloidalDiscModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4799.CycloidalDiscModalAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4799.CycloidalDiscModalAnalysis]':
        '''List[CycloidalDiscModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4799.CycloidalDiscModalAnalysis))
        return value
