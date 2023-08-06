﻿'''_7289.py

ExternalCADModelCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2313
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7158
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7262
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ExternalCADModelCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundAdvancedSystemDeflection',)


class ExternalCADModelCompoundAdvancedSystemDeflection(_7262.ComponentCompoundAdvancedSystemDeflection):
    '''ExternalCADModelCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2313.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2313.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_7158.ExternalCADModelAdvancedSystemDeflection]':
        '''List[ExternalCADModelAdvancedSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_7158.ExternalCADModelAdvancedSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_7158.ExternalCADModelAdvancedSystemDeflection]':
        '''List[ExternalCADModelAdvancedSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_7158.ExternalCADModelAdvancedSystemDeflection))
        return value
