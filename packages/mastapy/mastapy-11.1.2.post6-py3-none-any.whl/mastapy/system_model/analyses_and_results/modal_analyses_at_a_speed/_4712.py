﻿'''_4712.py

ConceptGearModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.gears import _2381
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6675
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4741
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'ConceptGearModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearModalAnalysisAtASpeed',)


class ConceptGearModalAnalysisAtASpeed(_4741.GearModalAnalysisAtASpeed):
    '''ConceptGearModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2381.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2381.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6675.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6675.ConceptGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
