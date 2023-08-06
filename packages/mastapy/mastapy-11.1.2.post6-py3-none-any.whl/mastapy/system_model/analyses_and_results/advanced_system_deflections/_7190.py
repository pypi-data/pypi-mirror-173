﻿'''_7190.py

PlanetaryConnectionAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _2149
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6765
from mastapy.system_model.analyses_and_results.system_deflections import _2644
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7204
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'PlanetaryConnectionAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionAdvancedSystemDeflection',)


class PlanetaryConnectionAdvancedSystemDeflection(_7204.ShaftToMountableComponentConnectionAdvancedSystemDeflection):
    '''PlanetaryConnectionAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2149.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2149.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6765.PlanetaryConnectionLoadCase':
        '''PlanetaryConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6765.PlanetaryConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2644.PlanetaryConnectionSystemDeflection]':
        '''List[PlanetaryConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2644.PlanetaryConnectionSystemDeflection))
        return value
