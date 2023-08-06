﻿'''_4679.py

BevelDifferentialSunGearCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4550
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4675
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'BevelDifferentialSunGearCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearCompoundModalAnalysisAtASpeed',)


class BevelDifferentialSunGearCompoundModalAnalysisAtASpeed(_4675.BevelDifferentialGearCompoundModalAnalysisAtASpeed):
    '''BevelDifferentialSunGearCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_4550.BevelDifferentialSunGearModalAnalysisAtASpeed]':
        '''List[BevelDifferentialSunGearModalAnalysisAtASpeed]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4550.BevelDifferentialSunGearModalAnalysisAtASpeed))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4550.BevelDifferentialSunGearModalAnalysisAtASpeed]':
        '''List[BevelDifferentialSunGearModalAnalysisAtASpeed]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4550.BevelDifferentialSunGearModalAnalysisAtASpeed))
        return value
