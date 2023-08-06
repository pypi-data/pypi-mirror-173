﻿'''_1199.py

Coil
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.electric_machines import _1200
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_COIL = python_net_import('SMT.MastaAPI.ElectricMachines', 'Coil')


__docformat__ = 'restructuredtext en'
__all__ = ('Coil',)


class Coil(_0.APIBase):
    '''Coil

    This is a mastapy class.
    '''

    TYPE = _COIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Coil.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def in_slot(self) -> 'int':
        '''int: 'InSlot' is the original name of this property.'''

        return self.wrapped.InSlot

    @in_slot.setter
    def in_slot(self, value: 'int'):
        self.wrapped.InSlot = int(value) if value else 0

    @property
    def out_slot(self) -> 'int':
        '''int: 'OutSlot' is the original name of this property.'''

        return self.wrapped.OutSlot

    @out_slot.setter
    def out_slot(self, value: 'int'):
        self.wrapped.OutSlot = int(value) if value else 0

    @property
    def phase(self) -> 'int':
        '''int: 'Phase' is the original name of this property.'''

        return self.wrapped.Phase

    @phase.setter
    def phase(self, value: 'int'):
        self.wrapped.Phase = int(value) if value else 0

    @property
    def in_slot_position(self) -> 'enum_with_selected_value.EnumWithSelectedValue_CoilPositionInSlot':
        '''enum_with_selected_value.EnumWithSelectedValue_CoilPositionInSlot: 'InSlotPosition' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_CoilPositionInSlot.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.InSlotPosition, value) if self.wrapped.InSlotPosition is not None else None

    @in_slot_position.setter
    def in_slot_position(self, value: 'enum_with_selected_value.EnumWithSelectedValue_CoilPositionInSlot.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CoilPositionInSlot.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.InSlotPosition = value

    @property
    def out_slot_position(self) -> 'enum_with_selected_value.EnumWithSelectedValue_CoilPositionInSlot':
        '''enum_with_selected_value.EnumWithSelectedValue_CoilPositionInSlot: 'OutSlotPosition' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_CoilPositionInSlot.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.OutSlotPosition, value) if self.wrapped.OutSlotPosition is not None else None

    @out_slot_position.setter
    def out_slot_position(self, value: 'enum_with_selected_value.EnumWithSelectedValue_CoilPositionInSlot.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CoilPositionInSlot.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.OutSlotPosition = value

    @property
    def mean_length_per_turn(self) -> 'float':
        '''float: 'MeanLengthPerTurn' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanLengthPerTurn

    @property
    def coil_pitch(self) -> 'float':
        '''float: 'CoilPitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CoilPitch

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

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
