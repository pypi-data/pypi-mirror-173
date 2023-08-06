﻿'''_5486.py

StraightBevelSunGearCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.mbd_analyses import _5348
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5479
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'StraightBevelSunGearCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearCompoundMultibodyDynamicsAnalysis',)


class StraightBevelSunGearCompoundMultibodyDynamicsAnalysis(_5479.StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis):
    '''StraightBevelSunGearCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_5348.StraightBevelSunGearMultibodyDynamicsAnalysis]':
        '''List[StraightBevelSunGearMultibodyDynamicsAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5348.StraightBevelSunGearMultibodyDynamicsAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5348.StraightBevelSunGearMultibodyDynamicsAnalysis]':
        '''List[StraightBevelSunGearMultibodyDynamicsAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5348.StraightBevelSunGearMultibodyDynamicsAnalysis))
        return value
