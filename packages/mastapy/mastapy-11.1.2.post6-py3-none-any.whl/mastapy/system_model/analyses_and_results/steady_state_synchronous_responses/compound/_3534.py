﻿'''_3534.py

CycloidalDiscCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2429
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3402
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3490
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'CycloidalDiscCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundSteadyStateSynchronousResponse',)


class CycloidalDiscCompoundSteadyStateSynchronousResponse(_3490.AbstractShaftCompoundSteadyStateSynchronousResponse):
    '''CycloidalDiscCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2429.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2429.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3402.CycloidalDiscSteadyStateSynchronousResponse]':
        '''List[CycloidalDiscSteadyStateSynchronousResponse]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3402.CycloidalDiscSteadyStateSynchronousResponse))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3402.CycloidalDiscSteadyStateSynchronousResponse]':
        '''List[CycloidalDiscSteadyStateSynchronousResponse]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3402.CycloidalDiscSteadyStateSynchronousResponse))
        return value
