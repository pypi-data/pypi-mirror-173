﻿'''_7153.py

CylindricalGearMeshAdvancedSystemDeflection
'''


from typing import List

from PIL.Image import Image

from mastapy.gears import _294
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _981, _974
from mastapy.gears.ltca.cylindrical import _824
from mastapy.math_utility import _1413
from mastapy.system_model.connections_and_sockets.gears import _2171
from mastapy.system_model.analyses_and_results.static_loads import _6697
from mastapy.gears.rating.cylindrical import _426
from mastapy.system_model.analyses_and_results.system_deflections import _2595
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7152, _7141, _7165
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CylindricalGearMeshAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshAdvancedSystemDeflection',)


class CylindricalGearMeshAdvancedSystemDeflection(_7165.GearMeshAdvancedSystemDeflection):
    '''CylindricalGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_flank(self) -> '_294.CylindricalFlanks':
        '''CylindricalFlanks: 'ActiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ActiveFlank)
        return constructor.new(_294.CylindricalFlanks)(value) if value is not None else None

    @property
    def inactive_flank(self) -> '_294.CylindricalFlanks':
        '''CylindricalFlanks: 'InactiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.InactiveFlank)
        return constructor.new(_294.CylindricalFlanks)(value) if value is not None else None

    @property
    def peak_to_peak_te(self) -> 'float':
        '''float: 'PeakToPeakTE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PeakToPeakTE

    @property
    def mean_te_excluding_backlash(self) -> 'float':
        '''float: 'MeanTEExcludingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanTEExcludingBacklash

    @property
    def torque_share(self) -> 'float':
        '''float: 'TorqueShare' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueShare

    @property
    def mean_mesh_tilt_stiffness(self) -> 'float':
        '''float: 'MeanMeshTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanMeshTiltStiffness

    @property
    def mean_mesh_stiffness(self) -> 'float':
        '''float: 'MeanMeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanMeshStiffness

    @property
    def peak_to_peak_mesh_stiffness(self) -> 'float':
        '''float: 'PeakToPeakMeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PeakToPeakMeshStiffness

    @property
    def mean_total_contact_ratio(self) -> 'float':
        '''float: 'MeanTotalContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanTotalContactRatio

    @property
    def maximum_contact_pressure(self) -> 'float':
        '''float: 'MaximumContactPressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumContactPressure

    @property
    def maximum_principal_root_stress_on_tension_side_from_gear_fe_model(self) -> 'List[float]':
        '''List[float]: 'MaximumPrincipalRootStressOnTensionSideFromGearFEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.MaximumPrincipalRootStressOnTensionSideFromGearFEModel)
        return value

    @property
    def face_load_factor_contact(self) -> 'float':
        '''float: 'FaceLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FaceLoadFactorContact

    @property
    def maximum_edge_stress(self) -> 'float':
        '''float: 'MaximumEdgeStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumEdgeStress

    @property
    def maximum_edge_stress_including_tip_contact(self) -> 'float':
        '''float: 'MaximumEdgeStressIncludingTipContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumEdgeStressIncludingTipContact

    @property
    def maximum_edge_stress_on_gear_a_including_tip_contact(self) -> 'float':
        '''float: 'MaximumEdgeStressOnGearAIncludingTipContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumEdgeStressOnGearAIncludingTipContact

    @property
    def maximum_edge_stress_on_gear_b_including_tip_contact(self) -> 'float':
        '''float: 'MaximumEdgeStressOnGearBIncludingTipContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumEdgeStressOnGearBIncludingTipContact

    @property
    def calculated_load_sharing_factor(self) -> 'float':
        '''float: 'CalculatedLoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculatedLoadSharingFactor

    @property
    def average_operating_transverse_contact_ratio_for_first_tooth_passing_period(self) -> 'float':
        '''float: 'AverageOperatingTransverseContactRatioForFirstToothPassingPeriod' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageOperatingTransverseContactRatioForFirstToothPassingPeriod

    @property
    def average_operating_axial_contact_ratio_for_first_tooth_passing_period(self) -> 'float':
        '''float: 'AverageOperatingAxialContactRatioForFirstToothPassingPeriod' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageOperatingAxialContactRatioForFirstToothPassingPeriod

    @property
    def use_advanced_ltca(self) -> 'bool':
        '''bool: 'UseAdvancedLTCA' is the original name of this property.'''

        return self.wrapped.UseAdvancedLTCA

    @use_advanced_ltca.setter
    def use_advanced_ltca(self, value: 'bool'):
        self.wrapped.UseAdvancedLTCA = bool(value) if value else False

    @property
    def contact_chart_max_pressure_gear_a(self) -> 'Image':
        '''Image: 'ContactChartMaxPressureGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.ContactChartMaxPressureGearA)
        return value

    @property
    def contact_chart_max_pressure_gear_b(self) -> 'Image':
        '''Image: 'ContactChartMaxPressureGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.ContactChartMaxPressureGearB)
        return value

    @property
    def contact_chart_gap_to_loaded_flank_gear_a(self) -> 'Image':
        '''Image: 'ContactChartGapToLoadedFlankGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.ContactChartGapToLoadedFlankGearA)
        return value

    @property
    def contact_chart_gap_to_loaded_flank_gear_b(self) -> 'Image':
        '''Image: 'ContactChartGapToLoadedFlankGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.ContactChartGapToLoadedFlankGearB)
        return value

    @property
    def contact_chart_gap_to_unloaded_flank_gear_a(self) -> 'Image':
        '''Image: 'ContactChartGapToUnloadedFlankGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.ContactChartGapToUnloadedFlankGearA)
        return value

    @property
    def contact_chart_gap_to_unloaded_flank_gear_b(self) -> 'Image':
        '''Image: 'ContactChartGapToUnloadedFlankGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.ContactChartGapToUnloadedFlankGearB)
        return value

    @property
    def gear_mesh_design(self) -> '_981.CylindricalGearMeshDesign':
        '''CylindricalGearMeshDesign: 'GearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_981.CylindricalGearMeshDesign)(self.wrapped.GearMeshDesign) if self.wrapped.GearMeshDesign is not None else None

    @property
    def point_with_maximum_contact_pressure(self) -> '_824.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'PointWithMaximumContactPressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_824.CylindricalGearMeshLoadedContactPoint)(self.wrapped.PointWithMaximumContactPressure) if self.wrapped.PointWithMaximumContactPressure is not None else None

    @property
    def transmission_error_fourier_series_for_first_tooth_passing_period(self) -> '_1413.FourierSeries':
        '''FourierSeries: 'TransmissionErrorFourierSeriesForFirstToothPassingPeriod' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1413.FourierSeries)(self.wrapped.TransmissionErrorFourierSeriesForFirstToothPassingPeriod) if self.wrapped.TransmissionErrorFourierSeriesForFirstToothPassingPeriod is not None else None

    @property
    def connection_design(self) -> '_2171.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2171.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6697.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6697.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def component_detailed_analysis(self) -> '_426.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_426.CylindricalGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None

    @property
    def cylindrical_gear_mesh_system_deflection_results(self) -> 'List[_2595.CylindricalGearMeshSystemDeflectionTimestep]':
        '''List[CylindricalGearMeshSystemDeflectionTimestep]: 'CylindricalGearMeshSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearMeshSystemDeflectionResults, constructor.new(_2595.CylindricalGearMeshSystemDeflectionTimestep))
        return value

    @property
    def gear_designs(self) -> 'List[_974.CylindricalGearDesign]':
        '''List[CylindricalGearDesign]: 'GearDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearDesigns, constructor.new(_974.CylindricalGearDesign))
        return value

    @property
    def cylindrical_gear_advanced_analyses(self) -> 'List[_7152.CylindricalGearAdvancedSystemDeflection]':
        '''List[CylindricalGearAdvancedSystemDeflection]: 'CylindricalGearAdvancedAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearAdvancedAnalyses, constructor.new(_7152.CylindricalGearAdvancedSystemDeflection))
        return value

    @property
    def max_pressure_contact_chart_for_each_tooth_pass_for_gear_a(self) -> 'List[_7141.ContactChartPerToothPass]':
        '''List[ContactChartPerToothPass]: 'MaxPressureContactChartForEachToothPassForGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MaxPressureContactChartForEachToothPassForGearA, constructor.new(_7141.ContactChartPerToothPass))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshAdvancedSystemDeflection]':
        '''List[CylindricalGearMeshAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshAdvancedSystemDeflection))
        return value

    def animation_of_max_pressure_contact_chart_for_each_tooth_pass_for_gear_a(self):
        ''' 'AnimationOfMaxPressureContactChartForEachToothPassForGearA' is the original name of this method.'''

        self.wrapped.AnimationOfMaxPressureContactChartForEachToothPassForGearA()

    def contact_chart_max_pressure_gear_a_as_text_file(self):
        ''' 'ContactChartMaxPressureGearAAsTextFile' is the original name of this method.'''

        self.wrapped.ContactChartMaxPressureGearAAsTextFile()

    def contact_chart_max_pressure_gear_b_as_text_file(self):
        ''' 'ContactChartMaxPressureGearBAsTextFile' is the original name of this method.'''

        self.wrapped.ContactChartMaxPressureGearBAsTextFile()

    def contact_chart_gap_to_loaded_flank_gear_a_as_text_file(self):
        ''' 'ContactChartGapToLoadedFlankGearAAsTextFile' is the original name of this method.'''

        self.wrapped.ContactChartGapToLoadedFlankGearAAsTextFile()

    def contact_chart_gap_to_loaded_flank_gear_b_as_text_file(self):
        ''' 'ContactChartGapToLoadedFlankGearBAsTextFile' is the original name of this method.'''

        self.wrapped.ContactChartGapToLoadedFlankGearBAsTextFile()

    def contact_chart_gap_to_unloaded_flank_gear_a_as_text_file(self):
        ''' 'ContactChartGapToUnloadedFlankGearAAsTextFile' is the original name of this method.'''

        self.wrapped.ContactChartGapToUnloadedFlankGearAAsTextFile()

    def contact_chart_gap_to_unloaded_flank_gear_b_as_text_file(self):
        ''' 'ContactChartGapToUnloadedFlankGearBAsTextFile' is the original name of this method.'''

        self.wrapped.ContactChartGapToUnloadedFlankGearBAsTextFile()
