﻿'''_6886.py

CycloidalDiscAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model.cycloidal import _2429
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6693
from mastapy.system_model.analyses_and_results.system_deflections import _2593
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6839
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'CycloidalDiscAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscAdvancedTimeSteppingAnalysisForModulation',)


class CycloidalDiscAdvancedTimeSteppingAnalysisForModulation(_6839.AbstractShaftAdvancedTimeSteppingAnalysisForModulation):
    '''CycloidalDiscAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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

    @property
    def system_deflection_results(self) -> '_2593.CycloidalDiscSystemDeflection':
        '''CycloidalDiscSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2593.CycloidalDiscSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
