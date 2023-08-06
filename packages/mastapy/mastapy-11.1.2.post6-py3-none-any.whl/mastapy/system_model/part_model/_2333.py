﻿'''_2333.py

PowerLoad
'''


from mastapy.math_utility.measured_data import _1467
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model import _2084
from mastapy.system_model.part_model import _2342, _2340
from mastapy.materials.efficiency import _269
from mastapy._internal.python_net import python_net_import

_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoad',)


class PowerLoad(_2340.VirtualComponent):
    '''PowerLoad

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoad.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def engine_torque_grid(self) -> '_1467.GriddedSurfaceAccessor':
        '''GriddedSurfaceAccessor: 'EngineTorqueGrid' is the original name of this property.'''

        return constructor.new(_1467.GriddedSurfaceAccessor)(self.wrapped.EngineTorqueGrid) if self.wrapped.EngineTorqueGrid is not None else None

    @engine_torque_grid.setter
    def engine_torque_grid(self, value: '_1467.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.EngineTorqueGrid = value

    @property
    def engine_fuel_consumption_grid(self) -> '_1467.GriddedSurfaceAccessor':
        '''GriddedSurfaceAccessor: 'EngineFuelConsumptionGrid' is the original name of this property.'''

        return constructor.new(_1467.GriddedSurfaceAccessor)(self.wrapped.EngineFuelConsumptionGrid) if self.wrapped.EngineFuelConsumptionGrid is not None else None

    @engine_fuel_consumption_grid.setter
    def engine_fuel_consumption_grid(self, value: '_1467.GriddedSurfaceAccessor'):
        value = value.wrapped if value else None
        self.wrapped.EngineFuelConsumptionGrid = value

    @property
    def positive_is_forwards(self) -> 'bool':
        '''bool: 'PositiveIsForwards' is the original name of this property.'''

        return self.wrapped.PositiveIsForwards

    @positive_is_forwards.setter
    def positive_is_forwards(self, value: 'bool'):
        self.wrapped.PositiveIsForwards = bool(value) if value else False

    @property
    def tyre_rolling_radius(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TyreRollingRadius' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TyreRollingRadius) if self.wrapped.TyreRollingRadius is not None else None

    @tyre_rolling_radius.setter
    def tyre_rolling_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TyreRollingRadius = value

    @property
    def torsional_stiffness(self) -> 'float':
        '''float: 'TorsionalStiffness' is the original name of this property.'''

        return self.wrapped.TorsionalStiffness

    @torsional_stiffness.setter
    def torsional_stiffness(self, value: 'float'):
        self.wrapped.TorsionalStiffness = float(value) if value else 0.0

    @property
    def power_load_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_PowerLoadType':
        '''enum_with_selected_value.EnumWithSelectedValue_PowerLoadType: 'PowerLoadType' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.PowerLoadType, value) if self.wrapped.PowerLoadType is not None else None

    @power_load_type.setter
    def power_load_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.PowerLoadType = value

    @property
    def number_of_blades(self) -> 'int':
        '''int: 'NumberOfBlades' is the original name of this property.'''

        return self.wrapped.NumberOfBlades

    @number_of_blades.setter
    def number_of_blades(self, value: 'int'):
        self.wrapped.NumberOfBlades = int(value) if value else 0

    @property
    def number_of_wheels(self) -> 'int':
        '''int: 'NumberOfWheels' is the original name of this property.'''

        return self.wrapped.NumberOfWheels

    @number_of_wheels.setter
    def number_of_wheels(self, value: 'int'):
        self.wrapped.NumberOfWheels = int(value) if value else 0

    @property
    def width_for_drawing(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'WidthForDrawing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.WidthForDrawing) if self.wrapped.WidthForDrawing is not None else None

    @width_for_drawing.setter
    def width_for_drawing(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.WidthForDrawing = value

    @property
    def inner_diameter_of_stator_teeth(self) -> 'float':
        '''float: 'InnerDiameterOfStatorTeeth' is the original name of this property.'''

        return self.wrapped.InnerDiameterOfStatorTeeth

    @inner_diameter_of_stator_teeth.setter
    def inner_diameter_of_stator_teeth(self, value: 'float'):
        self.wrapped.InnerDiameterOfStatorTeeth = float(value) if value else 0.0

    @property
    def number_of_slots(self) -> 'int':
        '''int: 'NumberOfSlots' is the original name of this property.'''

        return self.wrapped.NumberOfSlots

    @number_of_slots.setter
    def number_of_slots(self, value: 'int'):
        self.wrapped.NumberOfSlots = int(value) if value else 0

    @property
    def effective_length_of_stator(self) -> 'float':
        '''float: 'EffectiveLengthOfStator' is the original name of this property.'''

        return self.wrapped.EffectiveLengthOfStator

    @effective_length_of_stator.setter
    def effective_length_of_stator(self, value: 'float'):
        self.wrapped.EffectiveLengthOfStator = float(value) if value else 0.0

    @property
    def single_blade_details(self) -> '_2342.WindTurbineSingleBladeDetails':
        '''WindTurbineSingleBladeDetails: 'SingleBladeDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2342.WindTurbineSingleBladeDetails)(self.wrapped.SingleBladeDetails) if self.wrapped.SingleBladeDetails is not None else None

    @property
    def oil_pump_detail(self) -> '_269.OilPumpDetail':
        '''OilPumpDetail: 'OilPumpDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_269.OilPumpDetail)(self.wrapped.OilPumpDetail) if self.wrapped.OilPumpDetail is not None else None
