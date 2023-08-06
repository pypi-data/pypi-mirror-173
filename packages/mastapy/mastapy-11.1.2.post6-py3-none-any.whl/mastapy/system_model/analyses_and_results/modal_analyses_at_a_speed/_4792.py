﻿'''_4792.py

StraightBevelGearSetModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2408
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6797
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4791, _4790, _4700
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'StraightBevelGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetModalAnalysisAtASpeed',)


class StraightBevelGearSetModalAnalysisAtASpeed(_4700.BevelGearSetModalAnalysisAtASpeed):
    '''StraightBevelGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2408.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2408.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6797.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6797.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def straight_bevel_gears_modal_analysis_at_a_speed(self) -> 'List[_4791.StraightBevelGearModalAnalysisAtASpeed]':
        '''List[StraightBevelGearModalAnalysisAtASpeed]: 'StraightBevelGearsModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsModalAnalysisAtASpeed, constructor.new(_4791.StraightBevelGearModalAnalysisAtASpeed))
        return value

    @property
    def straight_bevel_meshes_modal_analysis_at_a_speed(self) -> 'List[_4790.StraightBevelGearMeshModalAnalysisAtASpeed]':
        '''List[StraightBevelGearMeshModalAnalysisAtASpeed]: 'StraightBevelMeshesModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesModalAnalysisAtASpeed, constructor.new(_4790.StraightBevelGearMeshModalAnalysisAtASpeed))
        return value
