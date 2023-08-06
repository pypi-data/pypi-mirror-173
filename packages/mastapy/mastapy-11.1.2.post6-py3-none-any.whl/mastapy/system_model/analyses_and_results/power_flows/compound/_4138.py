﻿'''_4138.py

TorqueConverterTurbineCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2470
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4009
from mastapy.system_model.analyses_and_results.power_flows.compound import _4057
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'TorqueConverterTurbineCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundPowerFlow',)


class TorqueConverterTurbineCompoundPowerFlow(_4057.CouplingHalfCompoundPowerFlow):
    '''TorqueConverterTurbineCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2470.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2470.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4009.TorqueConverterTurbinePowerFlow]':
        '''List[TorqueConverterTurbinePowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4009.TorqueConverterTurbinePowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4009.TorqueConverterTurbinePowerFlow]':
        '''List[TorqueConverterTurbinePowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4009.TorqueConverterTurbinePowerFlow))
        return value
