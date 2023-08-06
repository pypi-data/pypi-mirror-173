﻿'''_5303.py

KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.gears import _2400
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6751
from mastapy.system_model.analyses_and_results.mbd_analyses import _5297
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis(_5297.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2400.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2400.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6751.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6751.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
