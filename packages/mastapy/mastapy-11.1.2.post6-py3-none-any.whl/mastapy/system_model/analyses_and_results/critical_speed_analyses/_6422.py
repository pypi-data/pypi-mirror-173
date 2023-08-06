﻿'''_6422.py

CVTPulleyCriticalSpeedAnalysis
'''


from mastapy.system_model.part_model.couplings import _2447
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6468
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'CVTPulleyCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCriticalSpeedAnalysis',)


class CVTPulleyCriticalSpeedAnalysis(_6468.PulleyCriticalSpeedAnalysis):
    '''CVTPulleyCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2447.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2447.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None
