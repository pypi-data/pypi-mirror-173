﻿'''_2792.py

SpiralBevelGearSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.gears import _2256
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6645
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2709
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'SpiralBevelGearSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSteadyStateSynchronousResponseOnAShaft',)


class SpiralBevelGearSteadyStateSynchronousResponseOnAShaft(_2709.BevelGearSteadyStateSynchronousResponseOnAShaft):
    '''SpiralBevelGearSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2256.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2256.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6645.SpiralBevelGearLoadCase':
        '''SpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6645.SpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
