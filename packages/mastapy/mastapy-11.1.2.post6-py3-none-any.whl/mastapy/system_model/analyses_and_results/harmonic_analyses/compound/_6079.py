﻿'''_6079.py

SpringDamperHalfCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2461
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5913
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _6014
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'SpringDamperHalfCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfCompoundHarmonicAnalysis',)


class SpringDamperHalfCompoundHarmonicAnalysis(_6014.CouplingHalfCompoundHarmonicAnalysis):
    '''SpringDamperHalfCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfCompoundHarmonicAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_5913.SpringDamperHalfHarmonicAnalysis]':
        '''List[SpringDamperHalfHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5913.SpringDamperHalfHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5913.SpringDamperHalfHarmonicAnalysis]':
        '''List[SpringDamperHalfHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5913.SpringDamperHalfHarmonicAnalysis))
        return value
