﻿'''_842.py

CylindricalGearTIFFAnalysisDutyCycle
'''


from mastapy.gears.gear_two_d_fe_analysis import _843
from mastapy._internal import constructor
from mastapy.gears.analysis import _1146
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TIFF_ANALYSIS_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.GearTwoDFEAnalysis', 'CylindricalGearTIFFAnalysisDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearTIFFAnalysisDutyCycle',)


class CylindricalGearTIFFAnalysisDutyCycle(_1146.GearDesignAnalysis):
    '''CylindricalGearTIFFAnalysisDutyCycle

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_TIFF_ANALYSIS_DUTY_CYCLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearTIFFAnalysisDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis(self) -> '_843.CylindricalGearTwoDimensionalFEAnalysis':
        '''CylindricalGearTwoDimensionalFEAnalysis: 'Analysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_843.CylindricalGearTwoDimensionalFEAnalysis)(self.wrapped.Analysis) if self.wrapped.Analysis is not None else None
