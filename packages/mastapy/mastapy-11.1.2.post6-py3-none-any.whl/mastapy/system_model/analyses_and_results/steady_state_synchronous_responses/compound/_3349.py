﻿'''_3349.py

AssemblyCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2149, _2188
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3216
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3350, _3352, _3355, _3361,
    _3362, _3363, _3368, _3373,
    _3383, _3385, _3387, _3391,
    _3397, _3398, _3399, _3406,
    _3413, _3416, _3417, _3418,
    _3420, _3422, _3427, _3428,
    _3429, _3438, _3431, _3433,
    _3437, _3443, _3444, _3449,
    _3452, _3455, _3459, _3463,
    _3467, _3470, _3342
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'AssemblyCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSteadyStateSynchronousResponse',)


class AssemblyCompoundSteadyStateSynchronousResponse(_3342.AbstractAssemblyCompoundSteadyStateSynchronousResponse):
    '''AssemblyCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2149.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

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
    def assembly_analysis_cases_ready(self) -> 'List[_3216.AssemblySteadyStateSynchronousResponse]':
        '''List[AssemblySteadyStateSynchronousResponse]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3216.AssemblySteadyStateSynchronousResponse))
        return value

    @property
    def bearings(self) -> 'List[_3350.BearingCompoundSteadyStateSynchronousResponse]':
        '''List[BearingCompoundSteadyStateSynchronousResponse]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3350.BearingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def belt_drives(self) -> 'List[_3352.BeltDriveCompoundSteadyStateSynchronousResponse]':
        '''List[BeltDriveCompoundSteadyStateSynchronousResponse]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3352.BeltDriveCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3355.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3355.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bolts(self) -> 'List[_3361.BoltCompoundSteadyStateSynchronousResponse]':
        '''List[BoltCompoundSteadyStateSynchronousResponse]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3361.BoltCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bolted_joints(self) -> 'List[_3362.BoltedJointCompoundSteadyStateSynchronousResponse]':
        '''List[BoltedJointCompoundSteadyStateSynchronousResponse]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3362.BoltedJointCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def clutches(self) -> 'List[_3363.ClutchCompoundSteadyStateSynchronousResponse]':
        '''List[ClutchCompoundSteadyStateSynchronousResponse]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3363.ClutchCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_couplings(self) -> 'List[_3368.ConceptCouplingCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingCompoundSteadyStateSynchronousResponse]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3368.ConceptCouplingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3373.ConceptGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptGearSetCompoundSteadyStateSynchronousResponse]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3373.ConceptGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cv_ts(self) -> 'List[_3383.CVTCompoundSteadyStateSynchronousResponse]':
        '''List[CVTCompoundSteadyStateSynchronousResponse]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3383.CVTCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3385.CycloidalAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[CycloidalAssemblyCompoundSteadyStateSynchronousResponse]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3385.CycloidalAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3387.CycloidalDiscCompoundSteadyStateSynchronousResponse]':
        '''List[CycloidalDiscCompoundSteadyStateSynchronousResponse]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3387.CycloidalDiscCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3391.CylindricalGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[CylindricalGearSetCompoundSteadyStateSynchronousResponse]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3391.CylindricalGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3397.FaceGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[FaceGearSetCompoundSteadyStateSynchronousResponse]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3397.FaceGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def fe_parts(self) -> 'List[_3398.FEPartCompoundSteadyStateSynchronousResponse]':
        '''List[FEPartCompoundSteadyStateSynchronousResponse]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3398.FEPartCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3399.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3399.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3406.HypoidGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[HypoidGearSetCompoundSteadyStateSynchronousResponse]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3406.HypoidGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3413.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3413.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3416.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3416.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def mass_discs(self) -> 'List[_3417.MassDiscCompoundSteadyStateSynchronousResponse]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponse]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3417.MassDiscCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def measurement_components(self) -> 'List[_3418.MeasurementComponentCompoundSteadyStateSynchronousResponse]':
        '''List[MeasurementComponentCompoundSteadyStateSynchronousResponse]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3418.MeasurementComponentCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def oil_seals(self) -> 'List[_3420.OilSealCompoundSteadyStateSynchronousResponse]':
        '''List[OilSealCompoundSteadyStateSynchronousResponse]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3420.OilSealCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3422.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse]':
        '''List[PartToPartShearCouplingCompoundSteadyStateSynchronousResponse]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3422.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def planet_carriers(self) -> 'List[_3427.PlanetCarrierCompoundSteadyStateSynchronousResponse]':
        '''List[PlanetCarrierCompoundSteadyStateSynchronousResponse]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3427.PlanetCarrierCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def point_loads(self) -> 'List[_3428.PointLoadCompoundSteadyStateSynchronousResponse]':
        '''List[PointLoadCompoundSteadyStateSynchronousResponse]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3428.PointLoadCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def power_loads(self) -> 'List[_3429.PowerLoadCompoundSteadyStateSynchronousResponse]':
        '''List[PowerLoadCompoundSteadyStateSynchronousResponse]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3429.PowerLoadCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3438.ShaftHubConnectionCompoundSteadyStateSynchronousResponse]':
        '''List[ShaftHubConnectionCompoundSteadyStateSynchronousResponse]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3438.ShaftHubConnectionCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def ring_pins(self) -> 'List[_3431.RingPinsCompoundSteadyStateSynchronousResponse]':
        '''List[RingPinsCompoundSteadyStateSynchronousResponse]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3431.RingPinsCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3433.RollingRingAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[RollingRingAssemblyCompoundSteadyStateSynchronousResponse]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3433.RollingRingAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def shafts(self) -> 'List[_3437.ShaftCompoundSteadyStateSynchronousResponse]':
        '''List[ShaftCompoundSteadyStateSynchronousResponse]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3437.ShaftCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3443.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[SpiralBevelGearSetCompoundSteadyStateSynchronousResponse]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3443.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def spring_dampers(self) -> 'List[_3444.SpringDamperCompoundSteadyStateSynchronousResponse]':
        '''List[SpringDamperCompoundSteadyStateSynchronousResponse]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3444.SpringDamperCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3449.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3449.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3452.StraightBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelGearSetCompoundSteadyStateSynchronousResponse]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3452.StraightBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def synchronisers(self) -> 'List[_3455.SynchroniserCompoundSteadyStateSynchronousResponse]':
        '''List[SynchroniserCompoundSteadyStateSynchronousResponse]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3455.SynchroniserCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def torque_converters(self) -> 'List[_3459.TorqueConverterCompoundSteadyStateSynchronousResponse]':
        '''List[TorqueConverterCompoundSteadyStateSynchronousResponse]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3459.TorqueConverterCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3463.UnbalancedMassCompoundSteadyStateSynchronousResponse]':
        '''List[UnbalancedMassCompoundSteadyStateSynchronousResponse]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3463.UnbalancedMassCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3467.WormGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[WormGearSetCompoundSteadyStateSynchronousResponse]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3467.WormGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3470.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetCompoundSteadyStateSynchronousResponse]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3470.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3216.AssemblySteadyStateSynchronousResponse]':
        '''List[AssemblySteadyStateSynchronousResponse]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3216.AssemblySteadyStateSynchronousResponse))
        return value
