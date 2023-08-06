﻿'''_2737.py

ConceptGearSetCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2382
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2735, _2736, _2767
from mastapy.system_model.analyses_and_results.system_deflections import _2576
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ConceptGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundSystemDeflection',)


class ConceptGearSetCompoundSystemDeflection(_2767.GearSetCompoundSystemDeflection):
    '''ConceptGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2382.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2382.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2382.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2382.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def concept_gears_compound_system_deflection(self) -> 'List[_2735.ConceptGearCompoundSystemDeflection]':
        '''List[ConceptGearCompoundSystemDeflection]: 'ConceptGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundSystemDeflection, constructor.new(_2735.ConceptGearCompoundSystemDeflection))
        return value

    @property
    def concept_meshes_compound_system_deflection(self) -> 'List[_2736.ConceptGearMeshCompoundSystemDeflection]':
        '''List[ConceptGearMeshCompoundSystemDeflection]: 'ConceptMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundSystemDeflection, constructor.new(_2736.ConceptGearMeshCompoundSystemDeflection))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2576.ConceptGearSetSystemDeflection]':
        '''List[ConceptGearSetSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2576.ConceptGearSetSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2576.ConceptGearSetSystemDeflection]':
        '''List[ConceptGearSetSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2576.ConceptGearSetSystemDeflection))
        return value
