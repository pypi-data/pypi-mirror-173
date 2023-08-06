﻿'''_2382.py

ConceptGearSet
'''


from typing import List

from mastapy.gears.gear_designs.concept import _1130
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2381, _2392
from mastapy.system_model.connections_and_sockets.gears import _2167
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSet',)


class ConceptGearSet(_2392.GearSet):
    '''ConceptGearSet

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_set_design(self) -> '_1130.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1130.ConceptGearSetDesign)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign is not None else None

    @property
    def concept_gear_set_design(self) -> '_1130.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'ConceptGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1130.ConceptGearSetDesign)(self.wrapped.ConceptGearSetDesign) if self.wrapped.ConceptGearSetDesign is not None else None

    @property
    def concept_gears(self) -> 'List[_2381.ConceptGear]':
        '''List[ConceptGear]: 'ConceptGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGears, constructor.new(_2381.ConceptGear))
        return value

    @property
    def concept_meshes(self) -> 'List[_2167.ConceptGearMesh]':
        '''List[ConceptGearMesh]: 'ConceptMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshes, constructor.new(_2167.ConceptGearMesh))
        return value
