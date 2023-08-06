﻿'''_2671.py

StraightBevelGearMeshSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.gears import _2189
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6796
from mastapy.system_model.analyses_and_results.power_flows import _3996
from mastapy.gears.rating.straight_bevel import _370
from mastapy.system_model.analyses_and_results.system_deflections import _2561
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'StraightBevelGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshSystemDeflection',)


class StraightBevelGearMeshSystemDeflection(_2561.BevelGearMeshSystemDeflection):
    '''StraightBevelGearMeshSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2189.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2189.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_load_case(self) -> '_6796.StraightBevelGearMeshLoadCase':
        '''StraightBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6796.StraightBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3996.StraightBevelGearMeshPowerFlow':
        '''StraightBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3996.StraightBevelGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None

    @property
    def rating(self) -> '_370.StraightBevelGearMeshRating':
        '''StraightBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_370.StraightBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating is not None else None

    @property
    def component_detailed_analysis(self) -> '_370.StraightBevelGearMeshRating':
        '''StraightBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_370.StraightBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None
