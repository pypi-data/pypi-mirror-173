﻿'''_3427.py

PlanetCarrierCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2183
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3295
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3419
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'PlanetCarrierCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundSteadyStateSynchronousResponse',)


class PlanetCarrierCompoundSteadyStateSynchronousResponse(_3419.MountableComponentCompoundSteadyStateSynchronousResponse):
    '''PlanetCarrierCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2183.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2183.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3295.PlanetCarrierSteadyStateSynchronousResponse]':
        '''List[PlanetCarrierSteadyStateSynchronousResponse]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3295.PlanetCarrierSteadyStateSynchronousResponse))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3295.PlanetCarrierSteadyStateSynchronousResponse]':
        '''List[PlanetCarrierSteadyStateSynchronousResponse]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3295.PlanetCarrierSteadyStateSynchronousResponse))
        return value
