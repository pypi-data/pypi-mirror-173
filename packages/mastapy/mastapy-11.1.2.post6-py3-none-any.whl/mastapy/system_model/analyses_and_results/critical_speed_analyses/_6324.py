﻿"""_6324.py

FaceGearSetCriticalSpeedAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2278
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6610
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6322, _6323, _6329
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'FaceGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCriticalSpeedAnalysis',)


class FaceGearSetCriticalSpeedAnalysis(_6329.GearSetCriticalSpeedAnalysis):
    """FaceGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'FaceGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2278.FaceGearSet':
        """FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6610.FaceGearSetLoadCase':
        """FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def face_gears_critical_speed_analysis(self) -> 'List[_6322.FaceGearCriticalSpeedAnalysis]':
        """List[FaceGearCriticalSpeedAnalysis]: 'FaceGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearsCriticalSpeedAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def face_meshes_critical_speed_analysis(self) -> 'List[_6323.FaceGearMeshCriticalSpeedAnalysis]':
        """List[FaceGearMeshCriticalSpeedAnalysis]: 'FaceMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceMeshesCriticalSpeedAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
