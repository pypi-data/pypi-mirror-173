﻿'''_3844.py

BevelDifferentialGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2193
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3842, _3843, _3849
from mastapy.system_model.analyses_and_results.power_flows import _3711
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BevelDifferentialGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundPowerFlow',)


class BevelDifferentialGearSetCompoundPowerFlow(_3849.BevelGearSetCompoundPowerFlow):
    '''BevelDifferentialGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2193.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2193.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_power_flow(self) -> 'List[_3842.BevelDifferentialGearCompoundPowerFlow]':
        '''List[BevelDifferentialGearCompoundPowerFlow]: 'BevelDifferentialGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundPowerFlow, constructor.new(_3842.BevelDifferentialGearCompoundPowerFlow))
        return value

    @property
    def bevel_differential_meshes_compound_power_flow(self) -> 'List[_3843.BevelDifferentialGearMeshCompoundPowerFlow]':
        '''List[BevelDifferentialGearMeshCompoundPowerFlow]: 'BevelDifferentialMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundPowerFlow, constructor.new(_3843.BevelDifferentialGearMeshCompoundPowerFlow))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3711.BevelDifferentialGearSetPowerFlow]':
        '''List[BevelDifferentialGearSetPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3711.BevelDifferentialGearSetPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3711.BevelDifferentialGearSetPowerFlow]':
        '''List[BevelDifferentialGearSetPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3711.BevelDifferentialGearSetPowerFlow))
        return value
