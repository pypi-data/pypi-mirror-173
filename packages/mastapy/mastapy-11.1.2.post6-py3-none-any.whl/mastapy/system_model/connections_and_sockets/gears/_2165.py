﻿'''_2165.py

BevelGearMesh
'''


from mastapy.gears.gear_designs.bevel import _1133
from mastapy._internal import constructor
from mastapy.gears.gear_designs.zerol_bevel import _915
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _924
from mastapy.gears.gear_designs.straight_bevel import _928
from mastapy.gears.gear_designs.spiral_bevel import _932
from mastapy.system_model.connections_and_sockets.gears import _2161
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMesh',)


class BevelGearMesh(_2161.AGMAGleasonConicalGearMesh):
    '''BevelGearMesh

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_mesh_design(self) -> '_1133.BevelGearMeshDesign':
        '''BevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1133.BevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to BevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMeshDesign.__class__)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign is not None else None

    @property
    def bevel_gear_mesh_design_of_type_zerol_bevel_gear_mesh_design(self) -> '_915.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _915.ZerolBevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to ZerolBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMeshDesign.__class__)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign is not None else None

    @property
    def bevel_gear_mesh_design_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_924.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _924.StraightBevelDiffGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMeshDesign.__class__)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign is not None else None

    @property
    def bevel_gear_mesh_design_of_type_straight_bevel_gear_mesh_design(self) -> '_928.StraightBevelGearMeshDesign':
        '''StraightBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _928.StraightBevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to StraightBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMeshDesign.__class__)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign is not None else None

    @property
    def bevel_gear_mesh_design_of_type_spiral_bevel_gear_mesh_design(self) -> '_932.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _932.SpiralBevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to SpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMeshDesign.__class__)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign is not None else None
