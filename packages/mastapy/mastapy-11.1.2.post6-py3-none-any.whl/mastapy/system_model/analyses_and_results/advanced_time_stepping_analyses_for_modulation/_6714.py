﻿'''_6714.py

BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2229
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6512
from mastapy.system_model.analyses_and_results.system_deflections import _2410
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6712, _6713, _6719
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation',)


class BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation(_6719.BevelGearSetAdvancedTimeSteppingAnalysisForModulation):
    '''BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2229.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2229.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6512.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6512.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2410.BevelDifferentialGearSetSystemDeflection':
        '''BevelDifferentialGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2410.BevelDifferentialGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def bevel_differential_gears_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6712.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation]: 'BevelDifferentialGearsAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6712.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bevel_differential_meshes_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6713.BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'BevelDifferentialMeshesAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6713.BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value
