﻿'''_4131.py

SynchroniserCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2462
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4003
from mastapy.system_model.analyses_and_results.power_flows.compound import _4116
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'SynchroniserCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundPowerFlow',)


class SynchroniserCompoundPowerFlow(_4116.SpecialisedAssemblyCompoundPowerFlow):
    '''SynchroniserCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundPowerFlow.TYPE'):
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
    def assembly_analysis_cases_ready(self) -> 'List[_4003.SynchroniserPowerFlow]':
        '''List[SynchroniserPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4003.SynchroniserPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4003.SynchroniserPowerFlow]':
        '''List[SynchroniserPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4003.SynchroniserPowerFlow))
        return value
