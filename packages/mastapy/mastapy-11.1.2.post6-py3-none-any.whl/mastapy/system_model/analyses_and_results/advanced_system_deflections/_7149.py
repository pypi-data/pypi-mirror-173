﻿'''_7149.py

CycloidalDiscAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2429
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6693
from mastapy.system_model.analyses_and_results.system_deflections import _2593
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7102
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CycloidalDiscAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscAdvancedSystemDeflection',)


class CycloidalDiscAdvancedSystemDeflection(_7102.AbstractShaftAdvancedSystemDeflection):
    '''CycloidalDiscAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2429.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2429.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6693.CycloidalDiscLoadCase':
        '''CycloidalDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6693.CycloidalDiscLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2593.CycloidalDiscSystemDeflection]':
        '''List[CycloidalDiscSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2593.CycloidalDiscSystemDeflection))
        return value
