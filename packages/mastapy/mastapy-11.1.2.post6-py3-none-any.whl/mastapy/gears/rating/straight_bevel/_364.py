﻿'''_364.py

StraightBevelGearMeshRating
'''


from typing import List

from mastapy.gears.gear_designs.straight_bevel import _906
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.straight_bevel import _365
from mastapy.gears.rating.bevel import _508
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.StraightBevel', 'StraightBevelGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshRating',)


class StraightBevelGearMeshRating(_508.BevelGearMeshRating):
    '''StraightBevelGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def straight_bevel_gear_mesh(self) -> '_906.StraightBevelGearMeshDesign':
        '''StraightBevelGearMeshDesign: 'StraightBevelGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_906.StraightBevelGearMeshDesign)(self.wrapped.StraightBevelGearMesh) if self.wrapped.StraightBevelGearMesh is not None else None

    @property
    def straight_bevel_gear_ratings(self) -> 'List[_365.StraightBevelGearRating]':
        '''List[StraightBevelGearRating]: 'StraightBevelGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearRatings, constructor.new(_365.StraightBevelGearRating))
        return value
