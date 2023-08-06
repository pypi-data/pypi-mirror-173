﻿'''_6296.py

FaceGearCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2388
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6167
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6301
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'FaceGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundDynamicAnalysis',)


class FaceGearCompoundDynamicAnalysis(_6301.GearCompoundDynamicAnalysis):
    '''FaceGearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2388.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2388.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6167.FaceGearDynamicAnalysis]':
        '''List[FaceGearDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6167.FaceGearDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6167.FaceGearDynamicAnalysis]':
        '''List[FaceGearDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6167.FaceGearDynamicAnalysis))
        return value
