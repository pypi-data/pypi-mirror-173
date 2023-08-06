﻿'''_5802.py

BoltedJointHarmonicAnalysis
'''


from mastapy.system_model.part_model import _2305
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6665
from mastapy.system_model.analyses_and_results.system_deflections import _2564
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5907
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'BoltedJointHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointHarmonicAnalysis',)


class BoltedJointHarmonicAnalysis(_5907.SpecialisedAssemblyHarmonicAnalysis):
    '''BoltedJointHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2305.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2305.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6665.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6665.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2564.BoltedJointSystemDeflection':
        '''BoltedJointSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2564.BoltedJointSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
