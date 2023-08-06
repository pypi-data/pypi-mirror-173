﻿'''_5627.py

ConceptGearMeshHarmonicAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1987
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6483
from mastapy.system_model.analyses_and_results.system_deflections import _2390
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5670
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ConceptGearMeshHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshHarmonicAnalysis',)


class ConceptGearMeshHarmonicAnalysis(_5670.GearMeshHarmonicAnalysis):
    '''ConceptGearMeshHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1987.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6483.ConceptGearMeshLoadCase':
        '''ConceptGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6483.ConceptGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2390.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2390.ConceptGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
