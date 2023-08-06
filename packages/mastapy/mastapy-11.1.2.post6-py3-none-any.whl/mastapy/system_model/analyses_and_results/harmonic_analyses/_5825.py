﻿'''_5825.py

CVTHarmonicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2446
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2589
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5793
from mastapy._internal.python_net import python_net_import

_CVT_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'CVTHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTHarmonicAnalysis',)


class CVTHarmonicAnalysis(_5793.BeltDriveHarmonicAnalysis):
    '''CVTHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2446.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2446.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def system_deflection_results(self) -> '_2589.CVTSystemDeflection':
        '''CVTSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2589.CVTSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
