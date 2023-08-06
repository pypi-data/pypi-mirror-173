﻿'''_5350.py

SynchroniserMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2462
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6801
from mastapy.system_model.analyses_and_results.mbd_analyses import _5334
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'SynchroniserMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserMultibodyDynamicsAnalysis',)


class SynchroniserMultibodyDynamicsAnalysis(_5334.SpecialisedAssemblyMultibodyDynamicsAnalysis):
    '''SynchroniserMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2462.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2462.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6801.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6801.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None
