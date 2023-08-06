﻿'''_7148.py

CycloidalAssemblyAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2428
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6691
from mastapy.system_model.analyses_and_results.system_deflections import _2590
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7205
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CycloidalAssemblyAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyAdvancedSystemDeflection',)


class CycloidalAssemblyAdvancedSystemDeflection(_7205.SpecialisedAssemblyAdvancedSystemDeflection):
    '''CycloidalAssemblyAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2428.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2428.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6691.CycloidalAssemblyLoadCase':
        '''CycloidalAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6691.CycloidalAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2590.CycloidalAssemblySystemDeflection]':
        '''List[CycloidalAssemblySystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2590.CycloidalAssemblySystemDeflection))
        return value
