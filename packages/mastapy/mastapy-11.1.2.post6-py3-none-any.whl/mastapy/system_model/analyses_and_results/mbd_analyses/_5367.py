﻿'''_5367.py

ZerolBevelGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2414
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6820
from mastapy.system_model.analyses_and_results.mbd_analyses import _5366, _5365, _5242
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ZerolBevelGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetMultibodyDynamicsAnalysis',)


class ZerolBevelGearSetMultibodyDynamicsAnalysis(_5242.BevelGearSetMultibodyDynamicsAnalysis):
    '''ZerolBevelGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2414.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2414.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6820.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6820.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def gears(self) -> 'List[_5366.ZerolBevelGearMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5366.ZerolBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_gears_multibody_dynamics_analysis(self) -> 'List[_5366.ZerolBevelGearMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMultibodyDynamicsAnalysis]: 'ZerolBevelGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsMultibodyDynamicsAnalysis, constructor.new(_5366.ZerolBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_meshes_multibody_dynamics_analysis(self) -> 'List[_5365.ZerolBevelGearMeshMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMeshMultibodyDynamicsAnalysis]: 'ZerolBevelMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesMultibodyDynamicsAnalysis, constructor.new(_5365.ZerolBevelGearMeshMultibodyDynamicsAnalysis))
        return value
