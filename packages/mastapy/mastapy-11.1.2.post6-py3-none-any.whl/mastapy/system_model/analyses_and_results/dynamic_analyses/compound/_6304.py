﻿'''_6304.py

GuideDxfModelCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2316
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6175
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6268
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'GuideDxfModelCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundDynamicAnalysis',)


class GuideDxfModelCompoundDynamicAnalysis(_6268.ComponentCompoundDynamicAnalysis):
    '''GuideDxfModelCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2316.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2316.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6175.GuideDxfModelDynamicAnalysis]':
        '''List[GuideDxfModelDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6175.GuideDxfModelDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6175.GuideDxfModelDynamicAnalysis]':
        '''List[GuideDxfModelDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6175.GuideDxfModelDynamicAnalysis))
        return value
