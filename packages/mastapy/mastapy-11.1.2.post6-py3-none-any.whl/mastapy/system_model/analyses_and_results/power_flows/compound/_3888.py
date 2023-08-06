﻿'''_3888.py

FlexiblePinAssemblyCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2133
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3756
from mastapy.system_model.analyses_and_results.power_flows.compound import _3929
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'FlexiblePinAssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyCompoundPowerFlow',)


class FlexiblePinAssemblyCompoundPowerFlow(_3929.SpecialisedAssemblyCompoundPowerFlow):
    '''FlexiblePinAssemblyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2133.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.FlexiblePinAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2133.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3756.FlexiblePinAssemblyPowerFlow]':
        '''List[FlexiblePinAssemblyPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3756.FlexiblePinAssemblyPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3756.FlexiblePinAssemblyPowerFlow]':
        '''List[FlexiblePinAssemblyPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3756.FlexiblePinAssemblyPowerFlow))
        return value
