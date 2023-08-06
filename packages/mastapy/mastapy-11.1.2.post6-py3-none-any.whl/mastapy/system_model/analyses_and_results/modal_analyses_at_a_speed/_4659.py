﻿'''_4659.py

WormGearModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.gears import _2264
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6674
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4594
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'WormGearModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearModalAnalysisAtASpeed',)


class WormGearModalAnalysisAtASpeed(_4594.GearModalAnalysisAtASpeed):
    '''WormGearModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2264.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2264.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6674.WormGearLoadCase':
        '''WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6674.WormGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
