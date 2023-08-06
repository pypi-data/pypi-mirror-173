﻿'''_6044.py

KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2398
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5876
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _6041
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis',)


class KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis(_6041.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2398.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2398.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5876.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5876.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5876.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5876.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis))
        return value
