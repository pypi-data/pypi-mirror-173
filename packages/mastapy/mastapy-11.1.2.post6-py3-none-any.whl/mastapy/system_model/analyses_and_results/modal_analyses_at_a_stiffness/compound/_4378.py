﻿'''_4378.py

BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1983
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4247
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4383
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness',)


class BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness(_4383.BevelGearMeshCompoundModalAnalysisAtAStiffness):
    '''BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1983.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.BevelDifferentialGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1983.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_4247.BevelDifferentialGearMeshModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearMeshModalAnalysisAtAStiffness]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_4247.BevelDifferentialGearMeshModalAnalysisAtAStiffness))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_4247.BevelDifferentialGearMeshModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearMeshModalAnalysisAtAStiffness]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_4247.BevelDifferentialGearMeshModalAnalysisAtAStiffness))
        return value
