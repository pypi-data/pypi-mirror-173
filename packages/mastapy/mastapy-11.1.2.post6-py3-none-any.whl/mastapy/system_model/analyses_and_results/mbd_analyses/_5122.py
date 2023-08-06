﻿"""_5122.py

BeltConnectionMultibodyDynamicsAnalysis
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import _71
from mastapy.system_model.connections_and_sockets import _2019, _2024
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6544, _6577
from mastapy.system_model.analyses_and_results.mbd_analyses import _5184
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BeltConnectionMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionMultibodyDynamicsAnalysis',)


class BeltConnectionMultibodyDynamicsAnalysis(_5184.InterMountableComponentConnectionMultibodyDynamicsAnalysis):
    """BeltConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _BELT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'BeltConnectionMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def extension(self) -> 'float':
        """float: 'Extension' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Extension

        if temp is None:
            return None

        return temp

    @property
    def loading_status(self) -> '_71.LoadingStatus':
        """LoadingStatus: 'LoadingStatus' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadingStatus

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_71.LoadingStatus)(value) if value is not None else None

    @property
    def tension(self) -> 'float':
        """float: 'Tension' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Tension

        if temp is None:
            return None

        return temp

    @property
    def connection_design(self) -> '_2019.BeltConnection':
        """BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        if _2019.BeltConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6544.BeltConnectionLoadCase':
        """BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        if _6544.BeltConnectionLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connection_load_case to BeltConnectionLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
