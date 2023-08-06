﻿'''_2604.py

CylindricalMeshedGearSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2603, _2600, _2601, _2602,
    _2605, _2594, _2595, _2596
)
from mastapy.gears.ltca import _810
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESHED_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CylindricalMeshedGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshedGearSystemDeflection',)


class CylindricalMeshedGearSystemDeflection(_0.APIBase):
    '''CylindricalMeshedGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_MESHED_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalMeshedGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def change_in_operating_pitch_diameter_due_to_thermal_effects(self) -> 'float':
        '''float: 'ChangeInOperatingPitchDiameterDueToThermalEffects' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ChangeInOperatingPitchDiameterDueToThermalEffects

    @property
    def operating_tip_diameter(self) -> 'float':
        '''float: 'OperatingTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OperatingTipDiameter

    @property
    def minimum_operating_tip_clearance(self) -> 'float':
        '''float: 'MinimumOperatingTipClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumOperatingTipClearance

    @property
    def tilt_x(self) -> 'float':
        '''float: 'TiltX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TiltX

    @property
    def tilt_y(self) -> 'float':
        '''float: 'TiltY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TiltY

    @property
    def left_flank(self) -> '_2603.CylindricalMeshedGearFlankSystemDeflection':
        '''CylindricalMeshedGearFlankSystemDeflection: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2603.CylindricalMeshedGearFlankSystemDeflection)(self.wrapped.LeftFlank) if self.wrapped.LeftFlank is not None else None

    @property
    def right_flank(self) -> '_2603.CylindricalMeshedGearFlankSystemDeflection':
        '''CylindricalMeshedGearFlankSystemDeflection: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2603.CylindricalMeshedGearFlankSystemDeflection)(self.wrapped.RightFlank) if self.wrapped.RightFlank is not None else None

    @property
    def flanks(self) -> 'List[_2603.CylindricalMeshedGearFlankSystemDeflection]':
        '''List[CylindricalMeshedGearFlankSystemDeflection]: 'Flanks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Flanks, constructor.new(_2603.CylindricalMeshedGearFlankSystemDeflection))
        return value

    @property
    def tension_side_fillet_results(self) -> 'List[_810.GearRootFilletStressResults]':
        '''List[GearRootFilletStressResults]: 'TensionSideFilletResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TensionSideFilletResults, constructor.new(_810.GearRootFilletStressResults))
        return value

    @property
    def compression_side_fillet_results(self) -> 'List[_810.GearRootFilletStressResults]':
        '''List[GearRootFilletStressResults]: 'CompressionSideFilletResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CompressionSideFilletResults, constructor.new(_810.GearRootFilletStressResults))
        return value

    @property
    def cylindrical_gear_system_deflection(self) -> '_2600.CylindricalGearSystemDeflection':
        '''CylindricalGearSystemDeflection: 'CylindricalGearSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2600.CylindricalGearSystemDeflection.TYPE not in self.wrapped.CylindricalGearSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_system_deflection to CylindricalGearSystemDeflection. Expected: {}.'.format(self.wrapped.CylindricalGearSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearSystemDeflection.__class__)(self.wrapped.CylindricalGearSystemDeflection) if self.wrapped.CylindricalGearSystemDeflection is not None else None

    @property
    def cylindrical_gear_system_deflection_of_type_cylindrical_gear_system_deflection_timestep(self) -> '_2601.CylindricalGearSystemDeflectionTimestep':
        '''CylindricalGearSystemDeflectionTimestep: 'CylindricalGearSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2601.CylindricalGearSystemDeflectionTimestep.TYPE not in self.wrapped.CylindricalGearSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_system_deflection to CylindricalGearSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.CylindricalGearSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearSystemDeflection.__class__)(self.wrapped.CylindricalGearSystemDeflection) if self.wrapped.CylindricalGearSystemDeflection is not None else None

    @property
    def cylindrical_gear_system_deflection_of_type_cylindrical_gear_system_deflection_with_ltca_results(self) -> '_2602.CylindricalGearSystemDeflectionWithLTCAResults':
        '''CylindricalGearSystemDeflectionWithLTCAResults: 'CylindricalGearSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2602.CylindricalGearSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.CylindricalGearSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_system_deflection to CylindricalGearSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.CylindricalGearSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearSystemDeflection.__class__)(self.wrapped.CylindricalGearSystemDeflection) if self.wrapped.CylindricalGearSystemDeflection is not None else None

    @property
    def cylindrical_gear_system_deflection_of_type_cylindrical_planet_gear_system_deflection(self) -> '_2605.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'CylindricalGearSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2605.CylindricalPlanetGearSystemDeflection.TYPE not in self.wrapped.CylindricalGearSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_system_deflection to CylindricalPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.CylindricalGearSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearSystemDeflection.__class__)(self.wrapped.CylindricalGearSystemDeflection) if self.wrapped.CylindricalGearSystemDeflection is not None else None

    @property
    def other_cylindrical_gear_system_deflection(self) -> '_2600.CylindricalGearSystemDeflection':
        '''CylindricalGearSystemDeflection: 'OtherCylindricalGearSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2600.CylindricalGearSystemDeflection.TYPE not in self.wrapped.OtherCylindricalGearSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast other_cylindrical_gear_system_deflection to CylindricalGearSystemDeflection. Expected: {}.'.format(self.wrapped.OtherCylindricalGearSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OtherCylindricalGearSystemDeflection.__class__)(self.wrapped.OtherCylindricalGearSystemDeflection) if self.wrapped.OtherCylindricalGearSystemDeflection is not None else None

    @property
    def other_cylindrical_gear_system_deflection_of_type_cylindrical_gear_system_deflection_timestep(self) -> '_2601.CylindricalGearSystemDeflectionTimestep':
        '''CylindricalGearSystemDeflectionTimestep: 'OtherCylindricalGearSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2601.CylindricalGearSystemDeflectionTimestep.TYPE not in self.wrapped.OtherCylindricalGearSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast other_cylindrical_gear_system_deflection to CylindricalGearSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.OtherCylindricalGearSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OtherCylindricalGearSystemDeflection.__class__)(self.wrapped.OtherCylindricalGearSystemDeflection) if self.wrapped.OtherCylindricalGearSystemDeflection is not None else None

    @property
    def other_cylindrical_gear_system_deflection_of_type_cylindrical_gear_system_deflection_with_ltca_results(self) -> '_2602.CylindricalGearSystemDeflectionWithLTCAResults':
        '''CylindricalGearSystemDeflectionWithLTCAResults: 'OtherCylindricalGearSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2602.CylindricalGearSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.OtherCylindricalGearSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast other_cylindrical_gear_system_deflection to CylindricalGearSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.OtherCylindricalGearSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OtherCylindricalGearSystemDeflection.__class__)(self.wrapped.OtherCylindricalGearSystemDeflection) if self.wrapped.OtherCylindricalGearSystemDeflection is not None else None

    @property
    def other_cylindrical_gear_system_deflection_of_type_cylindrical_planet_gear_system_deflection(self) -> '_2605.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'OtherCylindricalGearSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2605.CylindricalPlanetGearSystemDeflection.TYPE not in self.wrapped.OtherCylindricalGearSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast other_cylindrical_gear_system_deflection to CylindricalPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.OtherCylindricalGearSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OtherCylindricalGearSystemDeflection.__class__)(self.wrapped.OtherCylindricalGearSystemDeflection) if self.wrapped.OtherCylindricalGearSystemDeflection is not None else None

    @property
    def cylindrical_gear_mesh_system_deflection(self) -> '_2594.CylindricalGearMeshSystemDeflection':
        '''CylindricalGearMeshSystemDeflection: 'CylindricalGearMeshSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2594.CylindricalGearMeshSystemDeflection.TYPE not in self.wrapped.CylindricalGearMeshSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_mesh_system_deflection to CylindricalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.CylindricalGearMeshSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearMeshSystemDeflection.__class__)(self.wrapped.CylindricalGearMeshSystemDeflection) if self.wrapped.CylindricalGearMeshSystemDeflection is not None else None

    @property
    def cylindrical_gear_mesh_system_deflection_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2595.CylindricalGearMeshSystemDeflectionTimestep':
        '''CylindricalGearMeshSystemDeflectionTimestep: 'CylindricalGearMeshSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2595.CylindricalGearMeshSystemDeflectionTimestep.TYPE not in self.wrapped.CylindricalGearMeshSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_mesh_system_deflection to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.CylindricalGearMeshSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearMeshSystemDeflection.__class__)(self.wrapped.CylindricalGearMeshSystemDeflection) if self.wrapped.CylindricalGearMeshSystemDeflection is not None else None

    @property
    def cylindrical_gear_mesh_system_deflection_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2596.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        '''CylindricalGearMeshSystemDeflectionWithLTCAResults: 'CylindricalGearMeshSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2596.CylindricalGearMeshSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.CylindricalGearMeshSystemDeflection.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_mesh_system_deflection to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.CylindricalGearMeshSystemDeflection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearMeshSystemDeflection.__class__)(self.wrapped.CylindricalGearMeshSystemDeflection) if self.wrapped.CylindricalGearMeshSystemDeflection is not None else None

    @property
    def both_flanks(self) -> '_2603.CylindricalMeshedGearFlankSystemDeflection':
        '''CylindricalMeshedGearFlankSystemDeflection: 'BothFlanks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2603.CylindricalMeshedGearFlankSystemDeflection)(self.wrapped.BothFlanks) if self.wrapped.BothFlanks is not None else None

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ReportNames, str)
        return value

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
