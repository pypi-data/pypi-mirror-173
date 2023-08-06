﻿"""_24.py

ShaftMaterial
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.shafts import (
    _7, _8, _12, _6,
    _11
)
from mastapy.materials import _245
from mastapy._internal.python_net import python_net_import

_SHAFT_MATERIAL = python_net_import('SMT.MastaAPI.Shafts', 'ShaftMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftMaterial',)


class ShaftMaterial(_245.Material):
    """ShaftMaterial

    This is a mastapy class.
    """

    TYPE = _SHAFT_MATERIAL

    def __init__(self, instance_to_wrap: 'ShaftMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def casting_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'CastingFactor' is the original name of this property."""

        temp = self.wrapped.CastingFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @casting_factor.setter
    def casting_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.CastingFactor = value

    @property
    def casting_factor_condition(self) -> '_7.CastingFactorCondition':
        """CastingFactorCondition: 'CastingFactorCondition' is the original name of this property."""

        temp = self.wrapped.CastingFactorCondition

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_7.CastingFactorCondition)(value) if value is not None else None

    @casting_factor_condition.setter
    def casting_factor_condition(self, value: '_7.CastingFactorCondition'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CastingFactorCondition = value

    @property
    def consequence_of_failure(self) -> '_8.ConsequenceOfFailure':
        """ConsequenceOfFailure: 'ConsequenceOfFailure' is the original name of this property."""

        temp = self.wrapped.ConsequenceOfFailure

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_8.ConsequenceOfFailure)(value) if value is not None else None

    @consequence_of_failure.setter
    def consequence_of_failure(self, value: '_8.ConsequenceOfFailure'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ConsequenceOfFailure = value

    @property
    def constant_rpmax(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ConstantRpmax' is the original name of this property."""

        temp = self.wrapped.ConstantRpmax

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @constant_rpmax.setter
    def constant_rpmax(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ConstantRpmax = value

    @property
    def curve_model(self) -> '_12.FkmSnCurveModel':
        """FkmSnCurveModel: 'CurveModel' is the original name of this property."""

        temp = self.wrapped.CurveModel

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_12.FkmSnCurveModel)(value) if value is not None else None

    @curve_model.setter
    def curve_model(self, value: '_12.FkmSnCurveModel'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CurveModel = value

    @property
    def endurance_limit(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'EnduranceLimit' is the original name of this property."""

        temp = self.wrapped.EnduranceLimit

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @endurance_limit.setter
    def endurance_limit(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.EnduranceLimit = value

    @property
    def factor_to_second_knee_point(self) -> 'float':
        """float: 'FactorToSecondKneePoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FactorToSecondKneePoint

        if temp is None:
            return None

        return temp

    @property
    def fatigue_strength_factor_for_normal_stress(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FatigueStrengthFactorForNormalStress' is the original name of this property."""

        temp = self.wrapped.FatigueStrengthFactorForNormalStress

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @fatigue_strength_factor_for_normal_stress.setter
    def fatigue_strength_factor_for_normal_stress(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FatigueStrengthFactorForNormalStress = value

    @property
    def fatigue_strength_factor_for_shear_stress(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FatigueStrengthFactorForShearStress' is the original name of this property."""

        temp = self.wrapped.FatigueStrengthFactorForShearStress

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @fatigue_strength_factor_for_shear_stress.setter
    def fatigue_strength_factor_for_shear_stress(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FatigueStrengthFactorForShearStress = value

    @property
    def fatigue_strength_under_reversed_bending_stresses(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FatigueStrengthUnderReversedBendingStresses' is the original name of this property."""

        temp = self.wrapped.FatigueStrengthUnderReversedBendingStresses

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @fatigue_strength_under_reversed_bending_stresses.setter
    def fatigue_strength_under_reversed_bending_stresses(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FatigueStrengthUnderReversedBendingStresses = value

    @property
    def fatigue_strength_under_reversed_compression_tension_stresses(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FatigueStrengthUnderReversedCompressionTensionStresses' is the original name of this property."""

        temp = self.wrapped.FatigueStrengthUnderReversedCompressionTensionStresses

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @fatigue_strength_under_reversed_compression_tension_stresses.setter
    def fatigue_strength_under_reversed_compression_tension_stresses(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FatigueStrengthUnderReversedCompressionTensionStresses = value

    @property
    def fatigue_strength_under_reversed_torsional_stresses(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FatigueStrengthUnderReversedTorsionalStresses' is the original name of this property."""

        temp = self.wrapped.FatigueStrengthUnderReversedTorsionalStresses

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @fatigue_strength_under_reversed_torsional_stresses.setter
    def fatigue_strength_under_reversed_torsional_stresses(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FatigueStrengthUnderReversedTorsionalStresses = value

    @property
    def first_exponent(self) -> 'float':
        """float: 'FirstExponent' is the original name of this property."""

        temp = self.wrapped.FirstExponent

        if temp is None:
            return None

        return temp

    @first_exponent.setter
    def first_exponent(self, value: 'float'):
        self.wrapped.FirstExponent = float(value) if value else 0.0

    @property
    def hardening_type_for_agma60016101e08(self) -> '_6.AGMAHardeningType':
        """AGMAHardeningType: 'HardeningTypeForAGMA60016101E08' is the original name of this property."""

        temp = self.wrapped.HardeningTypeForAGMA60016101E08

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_6.AGMAHardeningType)(value) if value is not None else None

    @hardening_type_for_agma60016101e08.setter
    def hardening_type_for_agma60016101e08(self, value: '_6.AGMAHardeningType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HardeningTypeForAGMA60016101E08 = value

    @property
    def has_hard_surface(self) -> 'bool':
        """bool: 'HasHardSurface' is the original name of this property."""

        temp = self.wrapped.HasHardSurface

        if temp is None:
            return None

        return temp

    @has_hard_surface.setter
    def has_hard_surface(self, value: 'bool'):
        self.wrapped.HasHardSurface = bool(value) if value else False

    @property
    def is_regularly_inspected(self) -> 'bool':
        """bool: 'IsRegularlyInspected' is the original name of this property."""

        temp = self.wrapped.IsRegularlyInspected

        if temp is None:
            return None

        return temp

    @is_regularly_inspected.setter
    def is_regularly_inspected(self, value: 'bool'):
        self.wrapped.IsRegularlyInspected = bool(value) if value else False

    @property
    def load_safety_factor(self) -> 'float':
        """float: 'LoadSafetyFactor' is the original name of this property."""

        temp = self.wrapped.LoadSafetyFactor

        if temp is None:
            return None

        return temp

    @load_safety_factor.setter
    def load_safety_factor(self, value: 'float'):
        self.wrapped.LoadSafetyFactor = float(value) if value else 0.0

    @property
    def lower_limit_of_the_effective_damage_sum(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'LowerLimitOfTheEffectiveDamageSum' is the original name of this property."""

        temp = self.wrapped.LowerLimitOfTheEffectiveDamageSum

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @lower_limit_of_the_effective_damage_sum.setter
    def lower_limit_of_the_effective_damage_sum(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.LowerLimitOfTheEffectiveDamageSum = value

    @property
    def material_fatigue_limit(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MaterialFatigueLimit' is the original name of this property."""

        temp = self.wrapped.MaterialFatigueLimit

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @material_fatigue_limit.setter
    def material_fatigue_limit(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MaterialFatigueLimit = value

    @property
    def material_fatigue_limit_shear(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MaterialFatigueLimitShear' is the original name of this property."""

        temp = self.wrapped.MaterialFatigueLimitShear

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @material_fatigue_limit_shear.setter
    def material_fatigue_limit_shear(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MaterialFatigueLimitShear = value

    @property
    def material_group(self) -> '_11.FkmMaterialGroup':
        """FkmMaterialGroup: 'MaterialGroup' is the original name of this property."""

        temp = self.wrapped.MaterialGroup

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_11.FkmMaterialGroup)(value) if value is not None else None

    @material_group.setter
    def material_group(self, value: '_11.FkmMaterialGroup'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MaterialGroup = value

    @property
    def material_safety_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MaterialSafetyFactor' is the original name of this property."""

        temp = self.wrapped.MaterialSafetyFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @material_safety_factor.setter
    def material_safety_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MaterialSafetyFactor = value

    @property
    def number_of_cycles_at_knee_point(self) -> 'float':
        """float: 'NumberOfCyclesAtKneePoint' is the original name of this property."""

        temp = self.wrapped.NumberOfCyclesAtKneePoint

        if temp is None:
            return None

        return temp

    @number_of_cycles_at_knee_point.setter
    def number_of_cycles_at_knee_point(self, value: 'float'):
        self.wrapped.NumberOfCyclesAtKneePoint = float(value) if value else 0.0

    @property
    def number_of_cycles_at_second_knee_point(self) -> 'float':
        """float: 'NumberOfCyclesAtSecondKneePoint' is the original name of this property."""

        temp = self.wrapped.NumberOfCyclesAtSecondKneePoint

        if temp is None:
            return None

        return temp

    @number_of_cycles_at_second_knee_point.setter
    def number_of_cycles_at_second_knee_point(self, value: 'float'):
        self.wrapped.NumberOfCyclesAtSecondKneePoint = float(value) if value else 0.0

    @property
    def second_exponent(self) -> 'float':
        """float: 'SecondExponent' is the original name of this property."""

        temp = self.wrapped.SecondExponent

        if temp is None:
            return None

        return temp

    @second_exponent.setter
    def second_exponent(self, value: 'float'):
        self.wrapped.SecondExponent = float(value) if value else 0.0

    @property
    def temperature_factor(self) -> 'float':
        """float: 'TemperatureFactor' is the original name of this property."""

        temp = self.wrapped.TemperatureFactor

        if temp is None:
            return None

        return temp

    @temperature_factor.setter
    def temperature_factor(self, value: 'float'):
        self.wrapped.TemperatureFactor = float(value) if value else 0.0

    @property
    def total_safety_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TotalSafetyFactor' is the original name of this property."""

        temp = self.wrapped.TotalSafetyFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @total_safety_factor.setter
    def total_safety_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TotalSafetyFactor = value

    @property
    def use_custom_sn_curve(self) -> 'bool':
        """bool: 'UseCustomSNCurve' is the original name of this property."""

        temp = self.wrapped.UseCustomSNCurve

        if temp is None:
            return None

        return temp

    @use_custom_sn_curve.setter
    def use_custom_sn_curve(self, value: 'bool'):
        self.wrapped.UseCustomSNCurve = bool(value) if value else False
