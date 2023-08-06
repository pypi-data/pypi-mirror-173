﻿'''_2567.py

CylindricalGearMeshCompoundSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets.gears import _1991
from mastapy.gears.rating.cylindrical import _426
from mastapy.system_model.analyses_and_results.system_deflections import _2411
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2579
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CylindricalGearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundSystemDeflection',)


class CylindricalGearMeshCompoundSystemDeflection(_2579.GearMeshCompoundSystemDeflection):
    '''CylindricalGearMeshCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_operating_backlash(self) -> 'float':
        '''float: 'MaximumOperatingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumOperatingBacklash

    @property
    def minimum_operating_backlash(self) -> 'float':
        '''float: 'MinimumOperatingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumOperatingBacklash

    @property
    def minimum_operating_transverse_contact_ratio(self) -> 'float':
        '''float: 'MinimumOperatingTransverseContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumOperatingTransverseContactRatio

    @property
    def minimum_operating_tip_root_clearance(self) -> 'float':
        '''float: 'MinimumOperatingTipRootClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumOperatingTipRootClearance

    @property
    def component_design(self) -> '_1991.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.CylindricalGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1991.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def cylindrical_mesh_rating(self) -> '_426.CylindricalMeshDutyCycleRating':
        '''CylindricalMeshDutyCycleRating: 'CylindricalMeshRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_426.CylindricalMeshDutyCycleRating)(self.wrapped.CylindricalMeshRating) if self.wrapped.CylindricalMeshRating else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_2411.CylindricalGearMeshSystemDeflectionWithLTCAResults]':
        '''List[CylindricalGearMeshSystemDeflectionWithLTCAResults]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_2411.CylindricalGearMeshSystemDeflectionWithLTCAResults))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCompoundSystemDeflection]':
        '''List[CylindricalGearMeshCompoundSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshCompoundSystemDeflection))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_2411.CylindricalGearMeshSystemDeflectionWithLTCAResults]':
        '''List[CylindricalGearMeshSystemDeflectionWithLTCAResults]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_2411.CylindricalGearMeshSystemDeflectionWithLTCAResults))
        return value
