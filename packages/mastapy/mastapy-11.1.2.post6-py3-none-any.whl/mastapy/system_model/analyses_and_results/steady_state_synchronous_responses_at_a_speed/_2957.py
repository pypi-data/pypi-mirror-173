﻿'''_2957.py

AssemblySteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2149, _2188
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6506, _6639
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _2958, _2960, _2962, _2970,
    _2969, _2973, _2978, _2980,
    _2992, _2993, _2996, _2998,
    _3004, _3006, _3007, _3013,
    _3020, _3023, _3025, _3026,
    _3028, _3032, _3035, _3036,
    _3037, _3045, _3039, _3041,
    _3046, _3050, _3054, _3057,
    _3060, _3067, _3070, _3072,
    _3075, _3078, _2950
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'AssemblySteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySteadyStateSynchronousResponseAtASpeed',)


class AssemblySteadyStateSynchronousResponseAtASpeed(_2950.AbstractAssemblySteadyStateSynchronousResponseAtASpeed):
    '''AssemblySteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblySteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2149.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6506.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6506.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def bearings(self) -> 'List[_2958.BearingSteadyStateSynchronousResponseAtASpeed]':
        '''List[BearingSteadyStateSynchronousResponseAtASpeed]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2958.BearingSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def belt_drives(self) -> 'List[_2960.BeltDriveSteadyStateSynchronousResponseAtASpeed]':
        '''List[BeltDriveSteadyStateSynchronousResponseAtASpeed]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2960.BeltDriveSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2962.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2962.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bolts(self) -> 'List[_2970.BoltSteadyStateSynchronousResponseAtASpeed]':
        '''List[BoltSteadyStateSynchronousResponseAtASpeed]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2970.BoltSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bolted_joints(self) -> 'List[_2969.BoltedJointSteadyStateSynchronousResponseAtASpeed]':
        '''List[BoltedJointSteadyStateSynchronousResponseAtASpeed]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2969.BoltedJointSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def clutches(self) -> 'List[_2973.ClutchSteadyStateSynchronousResponseAtASpeed]':
        '''List[ClutchSteadyStateSynchronousResponseAtASpeed]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2973.ClutchSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def concept_couplings(self) -> 'List[_2978.ConceptCouplingSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptCouplingSteadyStateSynchronousResponseAtASpeed]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2978.ConceptCouplingSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2980.ConceptGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptGearSetSteadyStateSynchronousResponseAtASpeed]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2980.ConceptGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cv_ts(self) -> 'List[_2992.CVTSteadyStateSynchronousResponseAtASpeed]':
        '''List[CVTSteadyStateSynchronousResponseAtASpeed]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2992.CVTSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_2993.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[CycloidalAssemblySteadyStateSynchronousResponseAtASpeed]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_2993.CycloidalAssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_2996.CycloidalDiscSteadyStateSynchronousResponseAtASpeed]':
        '''List[CycloidalDiscSteadyStateSynchronousResponseAtASpeed]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_2996.CycloidalDiscSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2998.CylindricalGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[CylindricalGearSetSteadyStateSynchronousResponseAtASpeed]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2998.CylindricalGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3004.FaceGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[FaceGearSetSteadyStateSynchronousResponseAtASpeed]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3004.FaceGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def fe_parts(self) -> 'List[_3006.FEPartSteadyStateSynchronousResponseAtASpeed]':
        '''List[FEPartSteadyStateSynchronousResponseAtASpeed]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3006.FEPartSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3007.FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3007.FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3013.HypoidGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[HypoidGearSetSteadyStateSynchronousResponseAtASpeed]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3013.HypoidGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3020.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3020.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3023.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3023.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def mass_discs(self) -> 'List[_3025.MassDiscSteadyStateSynchronousResponseAtASpeed]':
        '''List[MassDiscSteadyStateSynchronousResponseAtASpeed]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3025.MassDiscSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def measurement_components(self) -> 'List[_3026.MeasurementComponentSteadyStateSynchronousResponseAtASpeed]':
        '''List[MeasurementComponentSteadyStateSynchronousResponseAtASpeed]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3026.MeasurementComponentSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def oil_seals(self) -> 'List[_3028.OilSealSteadyStateSynchronousResponseAtASpeed]':
        '''List[OilSealSteadyStateSynchronousResponseAtASpeed]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3028.OilSealSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3032.PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed]':
        '''List[PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3032.PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def planet_carriers(self) -> 'List[_3035.PlanetCarrierSteadyStateSynchronousResponseAtASpeed]':
        '''List[PlanetCarrierSteadyStateSynchronousResponseAtASpeed]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3035.PlanetCarrierSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def point_loads(self) -> 'List[_3036.PointLoadSteadyStateSynchronousResponseAtASpeed]':
        '''List[PointLoadSteadyStateSynchronousResponseAtASpeed]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3036.PointLoadSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def power_loads(self) -> 'List[_3037.PowerLoadSteadyStateSynchronousResponseAtASpeed]':
        '''List[PowerLoadSteadyStateSynchronousResponseAtASpeed]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3037.PowerLoadSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3045.ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed]':
        '''List[ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3045.ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def ring_pins(self) -> 'List[_3039.RingPinsSteadyStateSynchronousResponseAtASpeed]':
        '''List[RingPinsSteadyStateSynchronousResponseAtASpeed]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3039.RingPinsSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3041.RollingRingAssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[RollingRingAssemblySteadyStateSynchronousResponseAtASpeed]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3041.RollingRingAssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def shafts(self) -> 'List[_3046.ShaftSteadyStateSynchronousResponseAtASpeed]':
        '''List[ShaftSteadyStateSynchronousResponseAtASpeed]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3046.ShaftSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3050.SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3050.SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def spring_dampers(self) -> 'List[_3054.SpringDamperSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpringDamperSteadyStateSynchronousResponseAtASpeed]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3054.SpringDamperSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3057.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3057.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3060.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3060.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def synchronisers(self) -> 'List[_3067.SynchroniserSteadyStateSynchronousResponseAtASpeed]':
        '''List[SynchroniserSteadyStateSynchronousResponseAtASpeed]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3067.SynchroniserSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def torque_converters(self) -> 'List[_3070.TorqueConverterSteadyStateSynchronousResponseAtASpeed]':
        '''List[TorqueConverterSteadyStateSynchronousResponseAtASpeed]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3070.TorqueConverterSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3072.UnbalancedMassSteadyStateSynchronousResponseAtASpeed]':
        '''List[UnbalancedMassSteadyStateSynchronousResponseAtASpeed]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3072.UnbalancedMassSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3075.WormGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[WormGearSetSteadyStateSynchronousResponseAtASpeed]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3075.WormGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3078.ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3078.ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value
