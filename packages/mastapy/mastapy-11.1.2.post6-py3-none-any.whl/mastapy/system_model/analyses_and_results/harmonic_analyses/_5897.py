﻿'''_5897.py

RingPinsHarmonicAnalysis
'''


from mastapy.system_model.part_model.cycloidal import _2430
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6776
from mastapy.system_model.analyses_and_results.system_deflections import _2649
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5884
from mastapy._internal.python_net import python_net_import

_RING_PINS_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'RingPinsHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsHarmonicAnalysis',)


class RingPinsHarmonicAnalysis(_5884.MountableComponentHarmonicAnalysis):
    '''RingPinsHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2430.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2430.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6776.RingPinsLoadCase':
        '''RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6776.RingPinsLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2649.RingPinsSystemDeflection':
        '''RingPinsSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2649.RingPinsSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
