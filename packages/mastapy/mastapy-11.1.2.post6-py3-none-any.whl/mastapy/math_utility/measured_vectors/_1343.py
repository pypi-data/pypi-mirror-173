﻿'''_1343.py

ForceAndDisplacementResults
'''


from mastapy.math_utility.measured_vectors import _1347, _1342
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_FORCE_AND_DISPLACEMENT_RESULTS = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'ForceAndDisplacementResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ForceAndDisplacementResults',)


class ForceAndDisplacementResults(_1342.AbstractForceAndDisplacementResults):
    '''ForceAndDisplacementResults

    This is a mastapy class.
    '''

    TYPE = _FORCE_AND_DISPLACEMENT_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ForceAndDisplacementResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def displacement(self) -> '_1347.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'Displacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1347.VectorWithLinearAndAngularComponents)(self.wrapped.Displacement) if self.wrapped.Displacement is not None else None
