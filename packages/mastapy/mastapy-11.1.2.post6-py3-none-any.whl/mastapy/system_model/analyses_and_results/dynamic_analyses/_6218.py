﻿'''_6218.py

SpringDamperHalfDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2461
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6790
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6152
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'SpringDamperHalfDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfDynamicAnalysis',)


class SpringDamperHalfDynamicAnalysis(_6152.CouplingHalfDynamicAnalysis):
    '''SpringDamperHalfDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2461.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2461.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6790.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6790.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
