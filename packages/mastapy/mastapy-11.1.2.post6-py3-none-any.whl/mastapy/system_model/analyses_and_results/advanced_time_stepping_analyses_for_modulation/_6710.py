﻿'''_6710.py

BeltConnectionAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.connections_and_sockets import _1983, _1988
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6508, _6541
from mastapy.system_model.analyses_and_results.system_deflections import _2407, _2440
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6767
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'BeltConnectionAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionAdvancedTimeSteppingAnalysisForModulation',)


class BeltConnectionAdvancedTimeSteppingAnalysisForModulation(_6767.InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation):
    '''BeltConnectionAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1983.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.BeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6508.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6508.BeltConnectionLoadCase.TYPE not in self.wrapped.ConnectionLoadCase.__class__.__mro__:
            raise CastException('Failed to cast connection_load_case to BeltConnectionLoadCase. Expected: {}.'.format(self.wrapped.ConnectionLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionLoadCase.__class__)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2407.BeltConnectionSystemDeflection':
        '''BeltConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2407.BeltConnectionSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BeltConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
