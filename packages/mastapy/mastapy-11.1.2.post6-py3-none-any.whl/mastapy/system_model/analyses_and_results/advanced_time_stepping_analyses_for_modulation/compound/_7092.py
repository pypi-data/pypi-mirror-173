﻿'''_7092.py

TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2470
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6963
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _7011
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation',)


class TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation(_7011.CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_6963.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation]':
        '''List[TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6963.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6963.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation]':
        '''List[TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6963.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation))
        return value
