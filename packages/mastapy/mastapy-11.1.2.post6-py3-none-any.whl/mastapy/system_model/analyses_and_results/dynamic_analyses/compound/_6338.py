﻿'''_6338.py

ShaftCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2343
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6209
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6244
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ShaftCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundDynamicAnalysis',)


class ShaftCompoundDynamicAnalysis(_6244.AbstractShaftCompoundDynamicAnalysis):
    '''ShaftCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2343.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2343.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6209.ShaftDynamicAnalysis]':
        '''List[ShaftDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6209.ShaftDynamicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundDynamicAnalysis]':
        '''List[ShaftCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6209.ShaftDynamicAnalysis]':
        '''List[ShaftDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6209.ShaftDynamicAnalysis))
        return value
