﻿'''_4364.py

KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2181
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4223
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4361
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool',)


class KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool(_4361.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool):
    '''KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2181.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def connection_design(self) -> '_2181.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_4223.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_4223.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_4223.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_4223.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool))
        return value
