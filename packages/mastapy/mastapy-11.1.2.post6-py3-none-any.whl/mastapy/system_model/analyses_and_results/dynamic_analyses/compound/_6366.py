﻿'''_6366.py

WormGearCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2411
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6237
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6301
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'WormGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundDynamicAnalysis',)


class WormGearCompoundDynamicAnalysis(_6301.GearCompoundDynamicAnalysis):
    '''WormGearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearCompoundDynamicAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_6237.WormGearDynamicAnalysis]':
        '''List[WormGearDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6237.WormGearDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6237.WormGearDynamicAnalysis]':
        '''List[WormGearDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6237.WormGearDynamicAnalysis))
        return value
