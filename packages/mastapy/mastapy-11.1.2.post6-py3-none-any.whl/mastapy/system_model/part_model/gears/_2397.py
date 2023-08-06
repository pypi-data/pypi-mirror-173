﻿'''_2397.py

KlingelnbergCycloPalloidConicalGearSet
'''


from mastapy.gears.gear_designs.klingelnberg_conical import _945
from mastapy._internal import constructor
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _937
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.klingelnberg_hypoid import _941
from mastapy.system_model.part_model.gears import _2384
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearSet',)


class KlingelnbergCycloPalloidConicalGearSet(_2384.ConicalGearSet):
    '''KlingelnbergCycloPalloidConicalGearSet

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conical_gear_set_design(self) -> '_945.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _945.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_937.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _937.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def conical_gear_set_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_941.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _941.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign is not None else None

    @property
    def klingelnberg_conical_gear_set_design(self) -> '_945.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'KlingelnbergConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _945.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.KlingelnbergConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast klingelnberg_conical_gear_set_design to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.KlingelnbergConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.KlingelnbergConicalGearSetDesign.__class__)(self.wrapped.KlingelnbergConicalGearSetDesign) if self.wrapped.KlingelnbergConicalGearSetDesign is not None else None

    @property
    def klingelnberg_conical_gear_set_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_937.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'KlingelnbergConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _937.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.KlingelnbergConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast klingelnberg_conical_gear_set_design to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.KlingelnbergConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.KlingelnbergConicalGearSetDesign.__class__)(self.wrapped.KlingelnbergConicalGearSetDesign) if self.wrapped.KlingelnbergConicalGearSetDesign is not None else None

    @property
    def klingelnberg_conical_gear_set_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_941.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'KlingelnbergConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _941.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.KlingelnbergConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast klingelnberg_conical_gear_set_design to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.KlingelnbergConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.KlingelnbergConicalGearSetDesign.__class__)(self.wrapped.KlingelnbergConicalGearSetDesign) if self.wrapped.KlingelnbergConicalGearSetDesign is not None else None
