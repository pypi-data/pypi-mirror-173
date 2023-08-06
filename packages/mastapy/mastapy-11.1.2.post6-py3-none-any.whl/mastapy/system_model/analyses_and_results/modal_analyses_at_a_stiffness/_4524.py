﻿'''_4524.py

SpiralBevelGearModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.gears import _2403
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6786
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4440
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'SpiralBevelGearModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearModalAnalysisAtAStiffness',)


class SpiralBevelGearModalAnalysisAtAStiffness(_4440.BevelGearModalAnalysisAtAStiffness):
    '''SpiralBevelGearModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2403.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2403.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6786.SpiralBevelGearLoadCase':
        '''SpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6786.SpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
