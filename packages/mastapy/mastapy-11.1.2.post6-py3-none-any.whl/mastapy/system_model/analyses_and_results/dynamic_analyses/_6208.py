﻿'''_6208.py

RootAssemblyDynamicAnalysis
'''


from mastapy.system_model.part_model import _2335
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _2486, _6120
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3408
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _2490
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4475
from mastapy.system_model.analyses_and_results.modal_analyses import _2489
from mastapy.system_model.analyses_and_results.harmonic_analyses import _2488
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'RootAssemblyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyDynamicAnalysis',)


class RootAssemblyDynamicAnalysis(_6120.AssemblyDynamicAnalysis):
    '''RootAssemblyDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2335.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2335.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def dynamic_analysis_inputs(self) -> '_2486.DynamicAnalysis':
        '''DynamicAnalysis: 'DynamicAnalysisInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2486.DynamicAnalysis.TYPE not in self.wrapped.DynamicAnalysisInputs.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_inputs to DynamicAnalysis. Expected: {}.'.format(self.wrapped.DynamicAnalysisInputs.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DynamicAnalysisInputs.__class__)(self.wrapped.DynamicAnalysisInputs) if self.wrapped.DynamicAnalysisInputs is not None else None
