﻿'''_5830.py

CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis
'''


from mastapy.system_model.connections_and_sockets.cycloidal import _2200
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6694
from mastapy.system_model.analyses_and_results.system_deflections import _2592
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5786
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis',)


class CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis(_5786.AbstractShaftToMountableComponentConnectionHarmonicAnalysis):
    '''CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2200.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6694.CycloidalDiscPlanetaryBearingConnectionLoadCase':
        '''CycloidalDiscPlanetaryBearingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6694.CycloidalDiscPlanetaryBearingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2592.CycloidalDiscPlanetaryBearingConnectionSystemDeflection':
        '''CycloidalDiscPlanetaryBearingConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2592.CycloidalDiscPlanetaryBearingConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
