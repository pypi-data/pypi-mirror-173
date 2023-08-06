﻿'''_4515.py

RollingRingAssemblyModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.couplings import _2457
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6778
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4522
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'RollingRingAssemblyModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyModalAnalysisAtAStiffness',)


class RollingRingAssemblyModalAnalysisAtAStiffness(_4522.SpecialisedAssemblyModalAnalysisAtAStiffness):
    '''RollingRingAssemblyModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2457.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2457.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6778.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6778.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None
