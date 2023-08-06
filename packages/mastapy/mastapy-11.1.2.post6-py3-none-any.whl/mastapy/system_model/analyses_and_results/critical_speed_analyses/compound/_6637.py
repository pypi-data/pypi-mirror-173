﻿'''_6637.py

ZerolBevelGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2414
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6635, _6636, _6527
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6508
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'ZerolBevelGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundCriticalSpeedAnalysis',)


class ZerolBevelGearSetCompoundCriticalSpeedAnalysis(_6527.BevelGearSetCompoundCriticalSpeedAnalysis):
    '''ZerolBevelGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2414.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2414.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2414.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2414.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def zerol_bevel_gears_compound_critical_speed_analysis(self) -> 'List[_6635.ZerolBevelGearCompoundCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearCompoundCriticalSpeedAnalysis]: 'ZerolBevelGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundCriticalSpeedAnalysis, constructor.new(_6635.ZerolBevelGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def zerol_bevel_meshes_compound_critical_speed_analysis(self) -> 'List[_6636.ZerolBevelGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearMeshCompoundCriticalSpeedAnalysis]: 'ZerolBevelMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6636.ZerolBevelGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6508.ZerolBevelGearSetCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6508.ZerolBevelGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6508.ZerolBevelGearSetCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6508.ZerolBevelGearSetCriticalSpeedAnalysis))
        return value
