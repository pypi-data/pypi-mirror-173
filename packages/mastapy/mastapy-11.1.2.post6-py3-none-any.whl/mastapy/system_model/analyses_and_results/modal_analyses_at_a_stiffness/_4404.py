﻿'''_4404.py

ZerolBevelGearModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.gears import _2266
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6677
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4293
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'ZerolBevelGearModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearModalAnalysisAtAStiffness',)


class ZerolBevelGearModalAnalysisAtAStiffness(_4293.BevelGearModalAnalysisAtAStiffness):
    '''ZerolBevelGearModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2266.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2266.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6677.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6677.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
