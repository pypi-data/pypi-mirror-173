﻿'''_5484.py

StraightBevelGearSetCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2408
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5482, _5483, _5392
from mastapy.system_model.analyses_and_results.mbd_analyses import _5346
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'StraightBevelGearSetCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundMultibodyDynamicsAnalysis',)


class StraightBevelGearSetCompoundMultibodyDynamicsAnalysis(_5392.BevelGearSetCompoundMultibodyDynamicsAnalysis):
    '''StraightBevelGearSetCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2408.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2408.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2408.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2408.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def straight_bevel_gears_compound_multibody_dynamics_analysis(self) -> 'List[_5482.StraightBevelGearCompoundMultibodyDynamicsAnalysis]':
        '''List[StraightBevelGearCompoundMultibodyDynamicsAnalysis]: 'StraightBevelGearsCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundMultibodyDynamicsAnalysis, constructor.new(_5482.StraightBevelGearCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_meshes_compound_multibody_dynamics_analysis(self) -> 'List[_5483.StraightBevelGearMeshCompoundMultibodyDynamicsAnalysis]':
        '''List[StraightBevelGearMeshCompoundMultibodyDynamicsAnalysis]: 'StraightBevelMeshesCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundMultibodyDynamicsAnalysis, constructor.new(_5483.StraightBevelGearMeshCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5346.StraightBevelGearSetMultibodyDynamicsAnalysis]':
        '''List[StraightBevelGearSetMultibodyDynamicsAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5346.StraightBevelGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5346.StraightBevelGearSetMultibodyDynamicsAnalysis]':
        '''List[StraightBevelGearSetMultibodyDynamicsAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5346.StraightBevelGearSetMultibodyDynamicsAnalysis))
        return value
