﻿'''_5499.py

WormGearSetCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2412
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5497, _5498, _5434
from mastapy.system_model.analyses_and_results.mbd_analyses import _5364
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'WormGearSetCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundMultibodyDynamicsAnalysis',)


class WormGearSetCompoundMultibodyDynamicsAnalysis(_5434.GearSetCompoundMultibodyDynamicsAnalysis):
    '''WormGearSetCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2412.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2412.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2412.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2412.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def worm_gears_compound_multibody_dynamics_analysis(self) -> 'List[_5497.WormGearCompoundMultibodyDynamicsAnalysis]':
        '''List[WormGearCompoundMultibodyDynamicsAnalysis]: 'WormGearsCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundMultibodyDynamicsAnalysis, constructor.new(_5497.WormGearCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def worm_meshes_compound_multibody_dynamics_analysis(self) -> 'List[_5498.WormGearMeshCompoundMultibodyDynamicsAnalysis]':
        '''List[WormGearMeshCompoundMultibodyDynamicsAnalysis]: 'WormMeshesCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundMultibodyDynamicsAnalysis, constructor.new(_5498.WormGearMeshCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5364.WormGearSetMultibodyDynamicsAnalysis]':
        '''List[WormGearSetMultibodyDynamicsAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5364.WormGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5364.WormGearSetMultibodyDynamicsAnalysis]':
        '''List[WormGearSetMultibodyDynamicsAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5364.WormGearSetMultibodyDynamicsAnalysis))
        return value
