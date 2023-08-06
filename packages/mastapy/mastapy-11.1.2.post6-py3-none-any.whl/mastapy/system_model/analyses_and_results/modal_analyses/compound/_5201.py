﻿'''_5201.py

StraightBevelGearCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2407
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _5056
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5109
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'StraightBevelGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearCompoundModalAnalysis',)


class StraightBevelGearCompoundModalAnalysis(_5109.BevelGearCompoundModalAnalysis):
    '''StraightBevelGearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2407.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2407.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5056.StraightBevelGearModalAnalysis]':
        '''List[StraightBevelGearModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5056.StraightBevelGearModalAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5056.StraightBevelGearModalAnalysis]':
        '''List[StraightBevelGearModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5056.StraightBevelGearModalAnalysis))
        return value
