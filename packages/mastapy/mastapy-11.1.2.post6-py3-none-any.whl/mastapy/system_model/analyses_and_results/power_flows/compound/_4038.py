﻿'''_4038.py

BoltedJointCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2305
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3904
from mastapy.system_model.analyses_and_results.power_flows.compound import _4116
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BoltedJointCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundPowerFlow',)


class BoltedJointCompoundPowerFlow(_4116.SpecialisedAssemblyCompoundPowerFlow):
    '''BoltedJointCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2305.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2305.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2305.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2305.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3904.BoltedJointPowerFlow]':
        '''List[BoltedJointPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3904.BoltedJointPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3904.BoltedJointPowerFlow]':
        '''List[BoltedJointPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3904.BoltedJointPowerFlow))
        return value
