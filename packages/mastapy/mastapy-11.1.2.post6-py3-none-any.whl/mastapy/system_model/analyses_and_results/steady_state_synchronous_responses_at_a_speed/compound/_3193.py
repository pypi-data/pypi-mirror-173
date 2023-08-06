﻿'''_3193.py

SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2315
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3067
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3178
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed',)


class SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed(_3178.SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed):
    '''SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2315.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2315.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2315.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2315.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3067.SynchroniserSteadyStateSynchronousResponseAtASpeed]':
        '''List[SynchroniserSteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3067.SynchroniserSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3067.SynchroniserSteadyStateSynchronousResponseAtASpeed]':
        '''List[SynchroniserSteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3067.SynchroniserSteadyStateSynchronousResponseAtASpeed))
        return value
