﻿'''_6585.py

MeasurementComponentCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2324
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6456
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6631
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'MeasurementComponentCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCompoundCriticalSpeedAnalysis',)


class MeasurementComponentCompoundCriticalSpeedAnalysis(_6631.VirtualComponentCompoundCriticalSpeedAnalysis):
    '''MeasurementComponentCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2324.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2324.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6456.MeasurementComponentCriticalSpeedAnalysis]':
        '''List[MeasurementComponentCriticalSpeedAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6456.MeasurementComponentCriticalSpeedAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6456.MeasurementComponentCriticalSpeedAnalysis]':
        '''List[MeasurementComponentCriticalSpeedAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6456.MeasurementComponentCriticalSpeedAnalysis))
        return value
