﻿'''_5266.py

CVTMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2446
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5234
from mastapy._internal.python_net import python_net_import

_CVT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'CVTMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTMultibodyDynamicsAnalysis',)


class CVTMultibodyDynamicsAnalysis(_5234.BeltDriveMultibodyDynamicsAnalysis):
    '''CVTMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2446.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2446.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None
