﻿'''_1240.py

NotchSpecification
'''


from typing import List

from mastapy.electric_machines import _1239
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_NOTCH_SPECIFICATION = python_net_import('SMT.MastaAPI.ElectricMachines', 'NotchSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('NotchSpecification',)


class NotchSpecification(_0.APIBase):
    '''NotchSpecification

    This is a mastapy class.
    '''

    TYPE = _NOTCH_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'NotchSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def notch_shape(self) -> '_1239.NotchShape':
        '''NotchShape: 'NotchShape' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.NotchShape)
        return constructor.new(_1239.NotchShape)(value) if value is not None else None

    @notch_shape.setter
    def notch_shape(self, value: '_1239.NotchShape'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.NotchShape = value

    @property
    def number_of_notches(self) -> 'int':
        '''int: 'NumberOfNotches' is the original name of this property.'''

        return self.wrapped.NumberOfNotches

    @number_of_notches.setter
    def number_of_notches(self, value: 'int'):
        self.wrapped.NumberOfNotches = int(value) if value else 0

    @property
    def first_notch_angle(self) -> 'float':
        '''float: 'FirstNotchAngle' is the original name of this property.'''

        return self.wrapped.FirstNotchAngle

    @first_notch_angle.setter
    def first_notch_angle(self, value: 'float'):
        self.wrapped.FirstNotchAngle = float(value) if value else 0.0

    @property
    def notch_diameter(self) -> 'float':
        '''float: 'NotchDiameter' is the original name of this property.'''

        return self.wrapped.NotchDiameter

    @notch_diameter.setter
    def notch_diameter(self, value: 'float'):
        self.wrapped.NotchDiameter = float(value) if value else 0.0

    @property
    def notch_offset_factor(self) -> 'float':
        '''float: 'NotchOffsetFactor' is the original name of this property.'''

        return self.wrapped.NotchOffsetFactor

    @notch_offset_factor.setter
    def notch_offset_factor(self, value: 'float'):
        self.wrapped.NotchOffsetFactor = float(value) if value else 0.0

    @property
    def notch_width_upper(self) -> 'float':
        '''float: 'NotchWidthUpper' is the original name of this property.'''

        return self.wrapped.NotchWidthUpper

    @notch_width_upper.setter
    def notch_width_upper(self, value: 'float'):
        self.wrapped.NotchWidthUpper = float(value) if value else 0.0

    @property
    def notch_width_lower(self) -> 'float':
        '''float: 'NotchWidthLower' is the original name of this property.'''

        return self.wrapped.NotchWidthLower

    @notch_width_lower.setter
    def notch_width_lower(self, value: 'float'):
        self.wrapped.NotchWidthLower = float(value) if value else 0.0

    @property
    def notch_depth(self) -> 'float':
        '''float: 'NotchDepth' is the original name of this property.'''

        return self.wrapped.NotchDepth

    @notch_depth.setter
    def notch_depth(self, value: 'float'):
        self.wrapped.NotchDepth = float(value) if value else 0.0

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
