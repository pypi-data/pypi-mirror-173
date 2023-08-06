﻿'''_4135.py

TorqueConverterCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2467
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4007
from mastapy.system_model.analyses_and_results.power_flows.compound import _4055
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'TorqueConverterCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterCompoundPowerFlow',)


class TorqueConverterCompoundPowerFlow(_4055.CouplingCompoundPowerFlow):
    '''TorqueConverterCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2467.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2467.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2467.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2467.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4007.TorqueConverterPowerFlow]':
        '''List[TorqueConverterPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4007.TorqueConverterPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4007.TorqueConverterPowerFlow]':
        '''List[TorqueConverterPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4007.TorqueConverterPowerFlow))
        return value
