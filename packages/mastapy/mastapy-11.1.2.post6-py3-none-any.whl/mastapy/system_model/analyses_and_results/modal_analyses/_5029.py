﻿'''_5029.py

PlanetaryConnectionModalAnalysis
'''


from mastapy.system_model.connections_and_sockets import _2149
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6765
from mastapy.system_model.analyses_and_results.system_deflections import _2644
from mastapy.system_model.analyses_and_results.modal_analyses import _5044
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'PlanetaryConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionModalAnalysis',)


class PlanetaryConnectionModalAnalysis(_5044.ShaftToMountableComponentConnectionModalAnalysis):
    '''PlanetaryConnectionModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionModalAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2644.PlanetaryConnectionSystemDeflection':
        '''PlanetaryConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2644.PlanetaryConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
