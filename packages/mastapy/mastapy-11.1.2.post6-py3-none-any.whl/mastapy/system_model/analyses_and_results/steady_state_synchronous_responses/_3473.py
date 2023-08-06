﻿'''_3473.py

SynchroniserHalfSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.couplings import _2464
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6800
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3474
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'SynchroniserHalfSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfSteadyStateSynchronousResponse',)


class SynchroniserHalfSteadyStateSynchronousResponse(_3474.SynchroniserPartSteadyStateSynchronousResponse):
    '''SynchroniserHalfSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2464.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2464.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6800.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6800.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
