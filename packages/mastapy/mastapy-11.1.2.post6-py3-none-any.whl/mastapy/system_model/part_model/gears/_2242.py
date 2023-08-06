﻿'''_2242.py

FaceGearSet
'''


from typing import List

from mastapy.gears.gear_designs.face import _935
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2241, _2245
from mastapy.system_model.connections_and_sockets.gears import _2026
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSet',)


class FaceGearSet(_2245.GearSet):
    '''FaceGearSet

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_set_design(self) -> '_935.FaceGearSetDesign':
        '''FaceGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_935.FaceGearSetDesign)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def face_gear_set_design(self) -> '_935.FaceGearSetDesign':
        '''FaceGearSetDesign: 'FaceGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_935.FaceGearSetDesign)(self.wrapped.FaceGearSetDesign) if self.wrapped.FaceGearSetDesign is not None else None

    @property
    def face_gears(self) -> 'List[_2241.FaceGear]':
        '''List[FaceGear]: 'FaceGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGears, constructor.new(_2241.FaceGear))
        return value

    @property
    def face_meshes(self) -> 'List[_2026.FaceGearMesh]':
        '''List[FaceGearMesh]: 'FaceMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshes, constructor.new(_2026.FaceGearMesh))
        return value
