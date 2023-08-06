﻿'''_6077.py

SpringDamperCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2460
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5914
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _6012
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'SpringDamperCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundHarmonicAnalysis',)


class SpringDamperCompoundHarmonicAnalysis(_6012.CouplingCompoundHarmonicAnalysis):
    '''SpringDamperCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2460.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2460.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2460.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2460.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5914.SpringDamperHarmonicAnalysis]':
        '''List[SpringDamperHarmonicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5914.SpringDamperHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5914.SpringDamperHarmonicAnalysis]':
        '''List[SpringDamperHarmonicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5914.SpringDamperHarmonicAnalysis))
        return value
