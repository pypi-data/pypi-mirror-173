﻿'''_7292.py

FaceGearSetCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2389
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7290, _7291, _7297
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7161
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'FaceGearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundAdvancedSystemDeflection',)


class FaceGearSetCompoundAdvancedSystemDeflection(_7297.GearSetCompoundAdvancedSystemDeflection):
    '''FaceGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2389.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2389.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2389.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2389.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def face_gears_compound_advanced_system_deflection(self) -> 'List[_7290.FaceGearCompoundAdvancedSystemDeflection]':
        '''List[FaceGearCompoundAdvancedSystemDeflection]: 'FaceGearsCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundAdvancedSystemDeflection, constructor.new(_7290.FaceGearCompoundAdvancedSystemDeflection))
        return value

    @property
    def face_meshes_compound_advanced_system_deflection(self) -> 'List[_7291.FaceGearMeshCompoundAdvancedSystemDeflection]':
        '''List[FaceGearMeshCompoundAdvancedSystemDeflection]: 'FaceMeshesCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundAdvancedSystemDeflection, constructor.new(_7291.FaceGearMeshCompoundAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_7161.FaceGearSetAdvancedSystemDeflection]':
        '''List[FaceGearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_7161.FaceGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_7161.FaceGearSetAdvancedSystemDeflection]':
        '''List[FaceGearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_7161.FaceGearSetAdvancedSystemDeflection))
        return value
