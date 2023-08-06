﻿'''_2472.py

ActiveFESubstructureSelectionGroup
'''


from mastapy.system_model.part_model.configurations import _2477, _2471
from mastapy.system_model.part_model import _2314
from mastapy.system_model.fe import _2244
from mastapy._internal.python_net import python_net_import

_ACTIVE_FE_SUBSTRUCTURE_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveFESubstructureSelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveFESubstructureSelectionGroup',)


class ActiveFESubstructureSelectionGroup(_2477.PartDetailConfiguration['_2471.ActiveFESubstructureSelection', '_2314.FEPart', '_2244.FESubstructure']):
    '''ActiveFESubstructureSelectionGroup

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_FE_SUBSTRUCTURE_SELECTION_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveFESubstructureSelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
