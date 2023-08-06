﻿'''_2269.py

RaceBearingFEWithSelection
'''


from mastapy.math_utility import _1399
from mastapy._internal import constructor
from mastapy.system_model.fe import _2267, _2222
from mastapy._internal.python_net import python_net_import

_RACE_BEARING_FE_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.FE', 'RaceBearingFEWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceBearingFEWithSelection',)


class RaceBearingFEWithSelection(_2222.BaseFEWithSelection):
    '''RaceBearingFEWithSelection

    This is a mastapy class.
    '''

    TYPE = _RACE_BEARING_FE_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RaceBearingFEWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def manual_alignment(self) -> '_1399.CoordinateSystemEditor':
        '''CoordinateSystemEditor: 'ManualAlignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1399.CoordinateSystemEditor)(self.wrapped.ManualAlignment) if self.wrapped.ManualAlignment is not None else None

    @property
    def race_bearing(self) -> '_2267.RaceBearingFE':
        '''RaceBearingFE: 'RaceBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2267.RaceBearingFE)(self.wrapped.RaceBearing) if self.wrapped.RaceBearing is not None else None
