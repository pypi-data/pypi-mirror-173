﻿'''_4143.py

WormGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.gears.rating.worm import _346
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2412
from mastapy.system_model.analyses_and_results.power_flows.compound import _4141, _4142, _4078
from mastapy.system_model.analyses_and_results.power_flows import _4014
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'WormGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundPowerFlow',)


class WormGearSetCompoundPowerFlow(_4078.GearSetCompoundPowerFlow):
    '''WormGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_duty_cycle_rating(self) -> '_346.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'GearSetDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_346.WormGearSetDutyCycleRating)(self.wrapped.GearSetDutyCycleRating) if self.wrapped.GearSetDutyCycleRating is not None else None

    @property
    def worm_gear_set_duty_cycle_rating(self) -> '_346.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'WormGearSetDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_346.WormGearSetDutyCycleRating)(self.wrapped.WormGearSetDutyCycleRating) if self.wrapped.WormGearSetDutyCycleRating is not None else None

    @property
    def component_design(self) -> '_2412.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2412.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2412.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2412.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def worm_gears_compound_power_flow(self) -> 'List[_4141.WormGearCompoundPowerFlow]':
        '''List[WormGearCompoundPowerFlow]: 'WormGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundPowerFlow, constructor.new(_4141.WormGearCompoundPowerFlow))
        return value

    @property
    def worm_meshes_compound_power_flow(self) -> 'List[_4142.WormGearMeshCompoundPowerFlow]':
        '''List[WormGearMeshCompoundPowerFlow]: 'WormMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundPowerFlow, constructor.new(_4142.WormGearMeshCompoundPowerFlow))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4014.WormGearSetPowerFlow]':
        '''List[WormGearSetPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4014.WormGearSetPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4014.WormGearSetPowerFlow]':
        '''List[WormGearSetPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4014.WormGearSetPowerFlow))
        return value
