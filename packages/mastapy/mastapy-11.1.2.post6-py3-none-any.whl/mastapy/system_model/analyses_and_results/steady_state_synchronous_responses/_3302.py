﻿'''_3302.py

RollingRingConnectionSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6637
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3275
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'RollingRingConnectionSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionSteadyStateSynchronousResponse',)


class RollingRingConnectionSteadyStateSynchronousResponse(_3275.InterMountableComponentConnectionSteadyStateSynchronousResponse):
    '''RollingRingConnectionSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2007.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6637.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6637.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionSteadyStateSynchronousResponse]':
        '''List[RollingRingConnectionSteadyStateSynchronousResponse]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionSteadyStateSynchronousResponse))
        return value
