﻿'''_7073.py

ClutchConnectionCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2024
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6940
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7089
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ClutchConnectionCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundAdvancedSystemDeflection',)


class ClutchConnectionCompoundAdvancedSystemDeflection(_7089.CouplingConnectionCompoundAdvancedSystemDeflection):
    '''ClutchConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2024.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2024.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2024.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2024.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_6940.ClutchConnectionAdvancedSystemDeflection]':
        '''List[ClutchConnectionAdvancedSystemDeflection]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_6940.ClutchConnectionAdvancedSystemDeflection))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_6940.ClutchConnectionAdvancedSystemDeflection]':
        '''List[ClutchConnectionAdvancedSystemDeflection]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_6940.ClutchConnectionAdvancedSystemDeflection))
        return value
