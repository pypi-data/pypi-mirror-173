﻿'''_7160.py

FaceGearMeshAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2173
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6718
from mastapy.gears.rating.face import _418
from mastapy.system_model.analyses_and_results.system_deflections import _2609
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7165
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'FaceGearMeshAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshAdvancedSystemDeflection',)


class FaceGearMeshAdvancedSystemDeflection(_7165.GearMeshAdvancedSystemDeflection):
    '''FaceGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2173.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2173.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6718.FaceGearMeshLoadCase':
        '''FaceGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6718.FaceGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def component_detailed_analysis(self) -> '_418.FaceGearMeshRating':
        '''FaceGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_418.FaceGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2609.FaceGearMeshSystemDeflection]':
        '''List[FaceGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2609.FaceGearMeshSystemDeflection))
        return value
