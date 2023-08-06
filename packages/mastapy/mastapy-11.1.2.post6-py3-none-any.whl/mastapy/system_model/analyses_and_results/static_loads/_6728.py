﻿'''_6728.py

GearSetLoadCase
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5284
from mastapy._internal.implicit import overridable
from mastapy.system_model.analyses_and_results.static_loads import (
    _6756, _6725, _6723, _6785
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model.gears import (
    _2392, _2374, _2376, _2380,
    _2382, _2384, _2386, _2389,
    _2395, _2397, _2399, _2401,
    _2402, _2404, _2406, _2408,
    _2412, _2414
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6844
from mastapy._internal.python_net import python_net_import

_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'GearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetLoadCase',)


class GearSetLoadCase(_6785.SpecialisedAssemblyLoadCase):
    '''GearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def excitation_data_is_up_to_date(self) -> 'bool':
        '''bool: 'ExcitationDataIsUpToDate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExcitationDataIsUpToDate

    @property
    def gear_mesh_stiffness_model(self) -> '_5284.GearMeshStiffnessModel':
        '''GearMeshStiffnessModel: 'GearMeshStiffnessModel' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.GearMeshStiffnessModel)
        return constructor.new(_5284.GearMeshStiffnessModel)(value) if value is not None else None

    @gear_mesh_stiffness_model.setter
    def gear_mesh_stiffness_model(self, value: '_5284.GearMeshStiffnessModel'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearMeshStiffnessModel = value

    @property
    def use_advanced_model_in_advanced_time_stepping_analysis_for_modulation(self) -> 'bool':
        '''bool: 'UseAdvancedModelInAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.'''

        return self.wrapped.UseAdvancedModelInAdvancedTimeSteppingAnalysisForModulation

    @use_advanced_model_in_advanced_time_stepping_analysis_for_modulation.setter
    def use_advanced_model_in_advanced_time_stepping_analysis_for_modulation(self, value: 'bool'):
        self.wrapped.UseAdvancedModelInAdvancedTimeSteppingAnalysisForModulation = bool(value) if value else False

    @property
    def mesh_stiffness_source(self) -> 'overridable.Overridable_MeshStiffnessSource':
        '''overridable.Overridable_MeshStiffnessSource: 'MeshStiffnessSource' is the original name of this property.'''

        value = overridable.Overridable_MeshStiffnessSource.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MeshStiffnessSource, value) if self.wrapped.MeshStiffnessSource is not None else None

    @mesh_stiffness_source.setter
    def mesh_stiffness_source(self, value: 'overridable.Overridable_MeshStiffnessSource.implicit_type()'):
        wrapper_type = overridable.Overridable_MeshStiffnessSource.wrapper_type()
        enclosed_type = overridable.Overridable_MeshStiffnessSource.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.MeshStiffnessSource = value

    @property
    def assembly_design(self) -> '_2392.GearSet':
        '''GearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2392.GearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to GearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_agma_gleason_conical_gear_set(self) -> '_2374.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2374.AGMAGleasonConicalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_bevel_differential_gear_set(self) -> '_2376.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2376.BevelDifferentialGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_bevel_gear_set(self) -> '_2380.BevelGearSet':
        '''BevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2380.BevelGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to BevelGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_concept_gear_set(self) -> '_2382.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2382.ConceptGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to ConceptGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_conical_gear_set(self) -> '_2384.ConicalGearSet':
        '''ConicalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2384.ConicalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to ConicalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_cylindrical_gear_set(self) -> '_2386.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2386.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_face_gear_set(self) -> '_2389.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2389.FaceGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to FaceGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_hypoid_gear_set(self) -> '_2395.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2395.HypoidGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to HypoidGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2397.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2397.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2399.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2399.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2401.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2401.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_planetary_gear_set(self) -> '_2402.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2402.PlanetaryGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_spiral_bevel_gear_set(self) -> '_2404.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2404.SpiralBevelGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_straight_bevel_diff_gear_set(self) -> '_2406.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2406.StraightBevelDiffGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_straight_bevel_gear_set(self) -> '_2408.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2408.StraightBevelGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_worm_gear_set(self) -> '_2412.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2412.WormGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to WormGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_design_of_type_zerol_bevel_gear_set(self) -> '_2414.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2414.ZerolBevelGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def advanced_time_stepping_analysis_for_modulation_options(self) -> '_6844.AdvancedTimeSteppingAnalysisForModulationOptions':
        '''AdvancedTimeSteppingAnalysisForModulationOptions: 'AdvancedTimeSteppingAnalysisForModulationOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6844.AdvancedTimeSteppingAnalysisForModulationOptions)(self.wrapped.AdvancedTimeSteppingAnalysisForModulationOptions) if self.wrapped.AdvancedTimeSteppingAnalysisForModulationOptions is not None else None

    @property
    def meshes_without_planetary_duplicates(self) -> 'List[_6725.GearMeshLoadCase]':
        '''List[GearMeshLoadCase]: 'MeshesWithoutPlanetaryDuplicates' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesWithoutPlanetaryDuplicates, constructor.new(_6725.GearMeshLoadCase))
        return value

    @property
    def gears(self) -> 'List[_6723.GearLoadCase]':
        '''List[GearLoadCase]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_6723.GearLoadCase))
        return value

    @property
    def gears_without_clones(self) -> 'List[_6723.GearLoadCase]':
        '''List[GearLoadCase]: 'GearsWithoutClones' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsWithoutClones, constructor.new(_6723.GearLoadCase))
        return value
