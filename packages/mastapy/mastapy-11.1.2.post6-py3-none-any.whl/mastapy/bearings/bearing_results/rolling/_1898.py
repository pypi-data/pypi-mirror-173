﻿'''_1898.py

LoadedRollerBearingRow
'''


from typing import List

from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.rolling import (
    _1897, _1857, _1862, _1865,
    _1873, _1877, _1889, _1892,
    _1908, _1911, _1917, _1926,
    _1842, _1902
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedRollerBearingRow',)


class LoadedRollerBearingRow(_1902.LoadedRollingBearingRow):
    '''LoadedRollerBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_ROLLER_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def roller_profile_warning(self) -> 'str':
        '''str: 'RollerProfileWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RollerProfileWarning

    @property
    def inner_race_profile_warning(self) -> 'str':
        '''str: 'InnerRaceProfileWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerRaceProfileWarning

    @property
    def outer_race_profile_warning(self) -> 'str':
        '''str: 'OuterRaceProfileWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterRaceProfileWarning

    @property
    def hertzian_contact_width_inner(self) -> 'float':
        '''float: 'HertzianContactWidthInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianContactWidthInner

    @property
    def hertzian_contact_width_outer(self) -> 'float':
        '''float: 'HertzianContactWidthOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianContactWidthOuter

    @property
    def maximum_shear_stress_outer(self) -> 'float':
        '''float: 'MaximumShearStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumShearStressOuter

    @property
    def maximum_shear_stress_inner(self) -> 'float':
        '''float: 'MaximumShearStressInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumShearStressInner

    @property
    def maximum_normal_edge_stress_inner(self) -> 'float':
        '''float: 'MaximumNormalEdgeStressInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalEdgeStressInner

    @property
    def maximum_normal_edge_stress_outer(self) -> 'float':
        '''float: 'MaximumNormalEdgeStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalEdgeStressOuter

    @property
    def shear_stress_chart_inner(self) -> 'Image':
        '''Image: 'ShearStressChartInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.ShearStressChartInner)
        return value

    @property
    def shear_stress_chart_outer(self) -> 'Image':
        '''Image: 'ShearStressChartOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.ShearStressChartOuter)
        return value

    @property
    def depth_of_maximum_shear_stress_chart_inner(self) -> 'Image':
        '''Image: 'DepthOfMaximumShearStressChartInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.DepthOfMaximumShearStressChartInner)
        return value

    @property
    def depth_of_maximum_shear_stress_chart_outer(self) -> 'Image':
        '''Image: 'DepthOfMaximumShearStressChartOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.DepthOfMaximumShearStressChartOuter)
        return value

    @property
    def loaded_bearing(self) -> '_1897.LoadedRollerBearingResults':
        '''LoadedRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1897.LoadedRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_asymmetric_spherical_roller_bearing_results(self) -> '_1857.LoadedAsymmetricSphericalRollerBearingResults':
        '''LoadedAsymmetricSphericalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1857.LoadedAsymmetricSphericalRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAsymmetricSphericalRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_axial_thrust_cylindrical_roller_bearing_results(self) -> '_1862.LoadedAxialThrustCylindricalRollerBearingResults':
        '''LoadedAxialThrustCylindricalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1862.LoadedAxialThrustCylindricalRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAxialThrustCylindricalRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_axial_thrust_needle_roller_bearing_results(self) -> '_1865.LoadedAxialThrustNeedleRollerBearingResults':
        '''LoadedAxialThrustNeedleRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1865.LoadedAxialThrustNeedleRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAxialThrustNeedleRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_crossed_roller_bearing_results(self) -> '_1873.LoadedCrossedRollerBearingResults':
        '''LoadedCrossedRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1873.LoadedCrossedRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedCrossedRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_cylindrical_roller_bearing_results(self) -> '_1877.LoadedCylindricalRollerBearingResults':
        '''LoadedCylindricalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1877.LoadedCylindricalRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedCylindricalRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_needle_roller_bearing_results(self) -> '_1889.LoadedNeedleRollerBearingResults':
        '''LoadedNeedleRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1889.LoadedNeedleRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedNeedleRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_non_barrel_roller_bearing_results(self) -> '_1892.LoadedNonBarrelRollerBearingResults':
        '''LoadedNonBarrelRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1892.LoadedNonBarrelRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedNonBarrelRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_spherical_roller_radial_bearing_results(self) -> '_1908.LoadedSphericalRollerRadialBearingResults':
        '''LoadedSphericalRollerRadialBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1908.LoadedSphericalRollerRadialBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedSphericalRollerRadialBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_spherical_roller_thrust_bearing_results(self) -> '_1911.LoadedSphericalRollerThrustBearingResults':
        '''LoadedSphericalRollerThrustBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1911.LoadedSphericalRollerThrustBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedSphericalRollerThrustBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_taper_roller_bearing_results(self) -> '_1917.LoadedTaperRollerBearingResults':
        '''LoadedTaperRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1917.LoadedTaperRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedTaperRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def loaded_bearing_of_type_loaded_toroidal_roller_bearing_results(self) -> '_1926.LoadedToroidalRollerBearingResults':
        '''LoadedToroidalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1926.LoadedToroidalRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedToroidalRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing is not None else None

    @property
    def lamina_dynamic_equivalent_loads(self) -> 'List[_1842.ForceAtLaminaGroupReportable]':
        '''List[ForceAtLaminaGroupReportable]: 'LaminaDynamicEquivalentLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LaminaDynamicEquivalentLoads, constructor.new(_1842.ForceAtLaminaGroupReportable))
        return value
