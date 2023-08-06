﻿'''_3170.py

RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2056
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3040
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3145
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed',)


class RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed(_3145.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed):
    '''RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2056.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2056.RingPinsToDiscConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def connection_design(self) -> '_2056.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2056.RingPinsToDiscConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3040.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed]':
        '''List[RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_3040.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3040.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed]':
        '''List[RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_3040.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed))
        return value
