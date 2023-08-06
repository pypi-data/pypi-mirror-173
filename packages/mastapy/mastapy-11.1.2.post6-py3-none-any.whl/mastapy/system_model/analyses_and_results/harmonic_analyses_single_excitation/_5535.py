﻿'''_5535.py

BevelDifferentialGearMeshHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.connections_and_sockets.gears import _2163
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6658
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5540
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'BevelDifferentialGearMeshHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshHarmonicAnalysisOfSingleExcitation',)


class BevelDifferentialGearMeshHarmonicAnalysisOfSingleExcitation(_5540.BevelGearMeshHarmonicAnalysisOfSingleExcitation):
    '''BevelDifferentialGearMeshHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2163.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6658.BevelDifferentialGearMeshLoadCase':
        '''BevelDifferentialGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6658.BevelDifferentialGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None
