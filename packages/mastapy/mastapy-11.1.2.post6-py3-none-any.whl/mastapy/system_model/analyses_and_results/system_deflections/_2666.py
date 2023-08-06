﻿'''_2666.py

SpringDamperHalfSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2461
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6790
from mastapy.system_model.analyses_and_results.power_flows import _3991
from mastapy.system_model.analyses_and_results.system_deflections import _2585
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SpringDamperHalfSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfSystemDeflection',)


class SpringDamperHalfSystemDeflection(_2585.CouplingHalfSystemDeflection):
    '''SpringDamperHalfSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2461.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2461.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6790.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6790.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3991.SpringDamperHalfPowerFlow':
        '''SpringDamperHalfPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3991.SpringDamperHalfPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None
