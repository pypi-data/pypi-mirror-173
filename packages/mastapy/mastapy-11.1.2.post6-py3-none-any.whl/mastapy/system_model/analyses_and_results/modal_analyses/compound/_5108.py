﻿'''_5108.py

BevelDifferentialSunGearCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses import _4955
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5104
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'BevelDifferentialSunGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearCompoundModalAnalysis',)


class BevelDifferentialSunGearCompoundModalAnalysis(_5104.BevelDifferentialGearCompoundModalAnalysis):
    '''BevelDifferentialSunGearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_4955.BevelDifferentialSunGearModalAnalysis]':
        '''List[BevelDifferentialSunGearModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4955.BevelDifferentialSunGearModalAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4955.BevelDifferentialSunGearModalAnalysis]':
        '''List[BevelDifferentialSunGearModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4955.BevelDifferentialSunGearModalAnalysis))
        return value
