﻿'''_2663.py

SpiralBevelGearSetSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2404
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6788
from mastapy.system_model.analyses_and_results.power_flows import _3989
from mastapy.gears.rating.spiral_bevel import _375
from mastapy.system_model.analyses_and_results.system_deflections import _2664, _2662, _2562
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SpiralBevelGearSetSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetSystemDeflection',)


class SpiralBevelGearSetSystemDeflection(_2562.BevelGearSetSystemDeflection):
    '''SpiralBevelGearSetSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2404.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2404.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6788.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6788.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3989.SpiralBevelGearSetPowerFlow':
        '''SpiralBevelGearSetPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3989.SpiralBevelGearSetPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None

    @property
    def rating(self) -> '_375.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_375.SpiralBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating is not None else None

    @property
    def component_detailed_analysis(self) -> '_375.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_375.SpiralBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None

    @property
    def spiral_bevel_gears_system_deflection(self) -> 'List[_2664.SpiralBevelGearSystemDeflection]':
        '''List[SpiralBevelGearSystemDeflection]: 'SpiralBevelGearsSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsSystemDeflection, constructor.new(_2664.SpiralBevelGearSystemDeflection))
        return value

    @property
    def spiral_bevel_meshes_system_deflection(self) -> 'List[_2662.SpiralBevelGearMeshSystemDeflection]':
        '''List[SpiralBevelGearMeshSystemDeflection]: 'SpiralBevelMeshesSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesSystemDeflection, constructor.new(_2662.SpiralBevelGearMeshSystemDeflection))
        return value
