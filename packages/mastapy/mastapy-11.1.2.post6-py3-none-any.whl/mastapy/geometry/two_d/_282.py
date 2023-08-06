﻿'''_282.py

CADFaceGroup
'''


from mastapy.geometry.two_d import _281
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CAD_FACE_GROUP = python_net_import('SMT.MastaAPI.Geometry.TwoD', 'CADFaceGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('CADFaceGroup',)


class CADFaceGroup(_0.APIBase):
    '''CADFaceGroup

    This is a mastapy class.
    '''

    TYPE = _CAD_FACE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CADFaceGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def add_face(self, moniker: 'str') -> '_281.CADFace':
        ''' 'AddFace' is the original name of this method.

        Args:
            moniker (str)

        Returns:
            mastapy.geometry.two_d.CADFace
        '''

        moniker = str(moniker)
        method_result = self.wrapped.AddFace(moniker if moniker else '')
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None
