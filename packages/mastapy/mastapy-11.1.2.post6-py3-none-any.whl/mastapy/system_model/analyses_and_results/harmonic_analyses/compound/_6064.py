﻿'''_6064.py

RingPinsCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2430
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5897
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _6052
from mastapy._internal.python_net import python_net_import

_RING_PINS_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'RingPinsCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsCompoundHarmonicAnalysis',)


class RingPinsCompoundHarmonicAnalysis(_6052.MountableComponentCompoundHarmonicAnalysis):
    '''RingPinsCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsCompoundHarmonicAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_5897.RingPinsHarmonicAnalysis]':
        '''List[RingPinsHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5897.RingPinsHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5897.RingPinsHarmonicAnalysis]':
        '''List[RingPinsHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5897.RingPinsHarmonicAnalysis))
        return value
