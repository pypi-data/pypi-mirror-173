﻿'''_6634.py

WormGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2412
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6632, _6633, _6569
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6505
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'WormGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundCriticalSpeedAnalysis',)


class WormGearSetCompoundCriticalSpeedAnalysis(_6569.GearSetCompoundCriticalSpeedAnalysis):
    '''WormGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundCriticalSpeedAnalysis.TYPE'):
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
    def worm_gears_compound_critical_speed_analysis(self) -> 'List[_6632.WormGearCompoundCriticalSpeedAnalysis]':
        '''List[WormGearCompoundCriticalSpeedAnalysis]: 'WormGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundCriticalSpeedAnalysis, constructor.new(_6632.WormGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def worm_meshes_compound_critical_speed_analysis(self) -> 'List[_6633.WormGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[WormGearMeshCompoundCriticalSpeedAnalysis]: 'WormMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6633.WormGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6505.WormGearSetCriticalSpeedAnalysis]':
        '''List[WormGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6505.WormGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6505.WormGearSetCriticalSpeedAnalysis]':
        '''List[WormGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6505.WormGearSetCriticalSpeedAnalysis))
        return value
