﻿'''_6632.py

WormGearCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2411
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6503
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6567
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'WormGearCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundCriticalSpeedAnalysis',)


class WormGearCompoundCriticalSpeedAnalysis(_6567.GearCompoundCriticalSpeedAnalysis):
    '''WormGearCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2411.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2411.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6503.WormGearCriticalSpeedAnalysis]':
        '''List[WormGearCriticalSpeedAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6503.WormGearCriticalSpeedAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6503.WormGearCriticalSpeedAnalysis]':
        '''List[WormGearCriticalSpeedAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6503.WormGearCriticalSpeedAnalysis))
        return value
