﻿'''_6175.py

GuideDxfModelDynamicAnalysis
'''


from mastapy.system_model.part_model import _2316
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6729
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6138
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'GuideDxfModelDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelDynamicAnalysis',)


class GuideDxfModelDynamicAnalysis(_6138.ComponentDynamicAnalysis):
    '''GuideDxfModelDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelDynamicAnalysis.TYPE'):
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
    def component_load_case(self) -> '_6729.GuideDxfModelLoadCase':
        '''GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6729.GuideDxfModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
