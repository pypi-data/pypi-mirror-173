﻿'''_7074.py

SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2460
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6945
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _7009
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation',)


class SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation(_7009.CouplingCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2460.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2460.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2460.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2460.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6945.SpringDamperAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpringDamperAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6945.SpringDamperAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6945.SpringDamperAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpringDamperAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6945.SpringDamperAdvancedTimeSteppingAnalysisForModulation))
        return value
