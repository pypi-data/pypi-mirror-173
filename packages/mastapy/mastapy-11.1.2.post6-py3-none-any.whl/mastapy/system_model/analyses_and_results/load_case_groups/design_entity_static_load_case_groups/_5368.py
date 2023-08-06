﻿'''_5368.py

GearSetStaticLoadCaseGroup
'''


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _5365, _5366, _5369
from mastapy.system_model.part_model.gears import _2239, _2237
from mastapy.system_model.analyses_and_results.static_loads import _6572, _6574, _6577
from mastapy.system_model.connections_and_sockets.gears import _2022
from mastapy._internal.python_net import python_net_import

_GEAR_SET_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups', 'GearSetStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetStaticLoadCaseGroup',)


TGearSet = TypeVar('TGearSet', bound='_2239.GearSet')
TGear = TypeVar('TGear', bound='_2237.Gear')
TGearStaticLoad = TypeVar('TGearStaticLoad', bound='_6572.GearLoadCase')
TGearMesh = TypeVar('TGearMesh', bound='_2022.GearMesh')
TGearMeshStaticLoad = TypeVar('TGearMeshStaticLoad', bound='_6574.GearMeshLoadCase')
TGearSetStaticLoad = TypeVar('TGearSetStaticLoad', bound='_6577.GearSetLoadCase')


class GearSetStaticLoadCaseGroup(_5369.PartStaticLoadCaseGroup, Generic[TGearSet, TGear, TGearStaticLoad, TGearMesh, TGearMeshStaticLoad, TGearSetStaticLoad]):
    '''GearSetStaticLoadCaseGroup

    This is a mastapy class.

    Generic Types:
        TGearSet
        TGear
        TGearStaticLoad
        TGearMesh
        TGearMeshStaticLoad
        TGearSetStaticLoad
    '''

    TYPE = _GEAR_SET_STATIC_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def part(self) -> 'TGearSet':
        '''TGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Part

    @property
    def gear_set(self) -> 'TGearSet':
        '''TGearSet: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GearSet

    @property
    def gears_load_cases(self) -> 'List[_5365.ComponentStaticLoadCaseGroup[TGear, TGearStaticLoad]]':
        '''List[ComponentStaticLoadCaseGroup[TGear, TGearStaticLoad]]: 'GearsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsLoadCases, constructor.new(_5365.ComponentStaticLoadCaseGroup)[TGear, TGearStaticLoad])
        return value

    @property
    def meshes_load_cases(self) -> 'List[_5366.ConnectionStaticLoadCaseGroup[TGearMesh, TGearMeshStaticLoad]]':
        '''List[ConnectionStaticLoadCaseGroup[TGearMesh, TGearMeshStaticLoad]]: 'MeshesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesLoadCases, constructor.new(_5366.ConnectionStaticLoadCaseGroup)[TGearMesh, TGearMeshStaticLoad])
        return value

    @property
    def part_load_cases(self) -> 'List[TGearSetStaticLoad]':
        '''List[TGearSetStaticLoad]: 'PartLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartLoadCases)
        return value

    @property
    def gear_set_load_cases(self) -> 'List[TGearSetStaticLoad]':
        '''List[TGearSetStaticLoad]: 'GearSetLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearSetLoadCases)
        return value
