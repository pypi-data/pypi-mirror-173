﻿'''_5206.py

SynchroniserCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2462
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _5061
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5191
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'SynchroniserCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundModalAnalysis',)


class SynchroniserCompoundModalAnalysis(_5191.SpecialisedAssemblyCompoundModalAnalysis):
    '''SynchroniserCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2462.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2462.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2462.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2462.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5061.SynchroniserModalAnalysis]':
        '''List[SynchroniserModalAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5061.SynchroniserModalAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5061.SynchroniserModalAnalysis]':
        '''List[SynchroniserModalAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5061.SynchroniserModalAnalysis))
        return value
