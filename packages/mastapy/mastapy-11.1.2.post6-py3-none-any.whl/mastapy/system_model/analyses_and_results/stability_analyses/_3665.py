﻿'''_3665.py

CycloidalDiscStabilityAnalysis
'''


from mastapy.system_model.part_model.cycloidal import _2429
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6693
from mastapy.system_model.analyses_and_results.stability_analyses import _3620
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'CycloidalDiscStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscStabilityAnalysis',)


class CycloidalDiscStabilityAnalysis(_3620.AbstractShaftStabilityAnalysis):
    '''CycloidalDiscStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2429.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2429.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6693.CycloidalDiscLoadCase':
        '''CycloidalDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6693.CycloidalDiscLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
