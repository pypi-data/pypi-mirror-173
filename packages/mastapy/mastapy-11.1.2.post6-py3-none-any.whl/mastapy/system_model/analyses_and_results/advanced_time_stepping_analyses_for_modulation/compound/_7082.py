﻿'''_7082.py

StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2408
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _7080, _7081, _6990
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6953
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation',)


class StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation(_6990.BevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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
    def straight_bevel_gears_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_7080.StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelGearsCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_7080.StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_meshes_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_7081.StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelMeshesCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_7081.StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6953.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6953.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6953.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6953.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
