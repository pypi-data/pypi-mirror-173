﻿'''_4913.py

SpringDamperCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2460
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4786
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4848
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'SpringDamperCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundModalAnalysisAtASpeed',)


class SpringDamperCompoundModalAnalysisAtASpeed(_4848.CouplingCompoundModalAnalysisAtASpeed):
    '''SpringDamperCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2460.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2460.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2460.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2460.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4786.SpringDamperModalAnalysisAtASpeed]':
        '''List[SpringDamperModalAnalysisAtASpeed]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4786.SpringDamperModalAnalysisAtASpeed))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4786.SpringDamperModalAnalysisAtASpeed]':
        '''List[SpringDamperModalAnalysisAtASpeed]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4786.SpringDamperModalAnalysisAtASpeed))
        return value
