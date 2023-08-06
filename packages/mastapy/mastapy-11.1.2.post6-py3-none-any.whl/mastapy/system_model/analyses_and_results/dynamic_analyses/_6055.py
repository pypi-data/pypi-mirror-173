﻿"""_6055.py

ExternalCADModelDynamicAnalysis
"""


from mastapy.system_model.part_model import _2202
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6607
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6027
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ExternalCADModelDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelDynamicAnalysis',)


class ExternalCADModelDynamicAnalysis(_6027.ComponentDynamicAnalysis):
    """ExternalCADModelDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _EXTERNAL_CAD_MODEL_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'ExternalCADModelDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2202.ExternalCADModel':
        """ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6607.ExternalCADModelLoadCase':
        """ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
