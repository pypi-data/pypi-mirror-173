﻿'''_2821.py

SynchroniserCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2462
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2679
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2806
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'SynchroniserCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundSystemDeflection',)


class SynchroniserCompoundSystemDeflection(_2806.SpecialisedAssemblyCompoundSystemDeflection):
    '''SynchroniserCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2462.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2462.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2462.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2462.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2679.SynchroniserSystemDeflection]':
        '''List[SynchroniserSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2679.SynchroniserSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2679.SynchroniserSystemDeflection]':
        '''List[SynchroniserSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2679.SynchroniserSystemDeflection))
        return value
