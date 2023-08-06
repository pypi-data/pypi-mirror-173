﻿'''_5866.py

PartToPartShearCouplingHalfCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2266
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5701
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5823
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'PartToPartShearCouplingHalfCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfCompoundHarmonicAnalysis',)


class PartToPartShearCouplingHalfCompoundHarmonicAnalysis(_5823.CouplingHalfCompoundHarmonicAnalysis):
    '''PartToPartShearCouplingHalfCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2266.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2266.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5701.PartToPartShearCouplingHalfHarmonicAnalysis]':
        '''List[PartToPartShearCouplingHalfHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5701.PartToPartShearCouplingHalfHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5701.PartToPartShearCouplingHalfHarmonicAnalysis]':
        '''List[PartToPartShearCouplingHalfHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5701.PartToPartShearCouplingHalfHarmonicAnalysis))
        return value
