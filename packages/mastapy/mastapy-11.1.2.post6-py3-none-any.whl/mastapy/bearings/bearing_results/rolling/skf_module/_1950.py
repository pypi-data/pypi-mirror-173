﻿'''_1950.py

Frequencies
'''


from mastapy.bearings.bearing_results.rolling.skf_module import _1963, _1951, _1965
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_FREQUENCIES = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'Frequencies')


__docformat__ = 'restructuredtext en'
__all__ = ('Frequencies',)


class Frequencies(_1965.SKFCalculationResult):
    '''Frequencies

    This is a mastapy class.
    '''

    TYPE = _FREQUENCIES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Frequencies.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rotational_frequency(self) -> '_1963.RotationalFrequency':
        '''RotationalFrequency: 'RotationalFrequency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1963.RotationalFrequency)(self.wrapped.RotationalFrequency) if self.wrapped.RotationalFrequency is not None else None

    @property
    def frequency_of_over_rolling(self) -> '_1951.FrequencyOfOverRolling':
        '''FrequencyOfOverRolling: 'FrequencyOfOverRolling' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1951.FrequencyOfOverRolling)(self.wrapped.FrequencyOfOverRolling) if self.wrapped.FrequencyOfOverRolling is not None else None
