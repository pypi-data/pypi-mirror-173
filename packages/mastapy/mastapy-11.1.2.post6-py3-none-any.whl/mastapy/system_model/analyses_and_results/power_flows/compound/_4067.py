﻿'''_4067.py

CylindricalGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.gears.rating.cylindrical import _432
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2386, _2402
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.power_flows.compound import _4065, _4066, _4078
from mastapy.system_model.analyses_and_results.power_flows import _3935
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CylindricalGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundPowerFlow',)


class CylindricalGearSetCompoundPowerFlow(_4078.GearSetCompoundPowerFlow):
    '''CylindricalGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_duty_cycle_rating(self) -> '_432.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'GearSetDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_432.CylindricalGearSetDutyCycleRating)(self.wrapped.GearSetDutyCycleRating) if self.wrapped.GearSetDutyCycleRating is not None else None

    @property
    def cylindrical_gear_set_duty_cycle_rating(self) -> '_432.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'CylindricalGearSetDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_432.CylindricalGearSetDutyCycleRating)(self.wrapped.CylindricalGearSetDutyCycleRating) if self.wrapped.CylindricalGearSetDutyCycleRating is not None else None

    @property
    def component_design(self) -> '_2386.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2386.CylindricalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2386.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2386.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def ratings_for_all_designs(self) -> 'List[_432.CylindricalGearSetDutyCycleRating]':
        '''List[CylindricalGearSetDutyCycleRating]: 'RatingsForAllDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RatingsForAllDesigns, constructor.new(_432.CylindricalGearSetDutyCycleRating))
        return value

    @property
    def cylindrical_gears_compound_power_flow(self) -> 'List[_4065.CylindricalGearCompoundPowerFlow]':
        '''List[CylindricalGearCompoundPowerFlow]: 'CylindricalGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundPowerFlow, constructor.new(_4065.CylindricalGearCompoundPowerFlow))
        return value

    @property
    def cylindrical_meshes_compound_power_flow(self) -> 'List[_4066.CylindricalGearMeshCompoundPowerFlow]':
        '''List[CylindricalGearMeshCompoundPowerFlow]: 'CylindricalMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundPowerFlow, constructor.new(_4066.CylindricalGearMeshCompoundPowerFlow))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3935.CylindricalGearSetPowerFlow]':
        '''List[CylindricalGearSetPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3935.CylindricalGearSetPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3935.CylindricalGearSetPowerFlow]':
        '''List[CylindricalGearSetPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3935.CylindricalGearSetPowerFlow))
        return value
