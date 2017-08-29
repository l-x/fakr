from collections import Sequence, Mapping
from functools import reduce
from operator import mul
from hashlib import md5


class CompoundMappingSequence(Sequence):

    def __init__(self, mapping_factory: callable=dict, *partitions: Sequence) -> None:
        self.__mapping_class=mapping_factory
        self.__partitions=partitions

        self.__list_lengths=[len(i) for i in self.__partitions]
        self.__len=reduce(mul, self.__list_lengths)

    def __len__(self) -> int:
        return self.__len

    def __create_guid(self, id: int) -> str:
        hexdigest=md5(str(id).encode()).hexdigest()

        return '-'.join([
            hexdigest[0:8],
            hexdigest[8:12],
            hexdigest[12:16],
            hexdigest[16:20],
            hexdigest[20:32]
        ])

    def __getitem__(self, index: int) -> Mapping:
        d = dict(
            id=index,
            guid=self.__create_guid(index),
        )

        for key, i in enumerate(self.__calculate_indices(index)):
            d.update(self.__partitions[key][i])

        return self.__mapping_class(**d)

    def __calculate_indices(self, item: int, lengths:Sequence=None) -> Sequence:
        if lengths is None:
            return self.__calculate_indices(item, self.__list_lengths)

        if len(lengths) == 0:
            raise IndexError('list index out of range')

        if item < lengths[0]:
            return [item]+[0]*(len(self.__partitions)-1)

        indices=[item % lengths[0]]
        indices.extend(self.__calculate_indices(int(item / lengths[0]), lengths[1:]))

        return (indices + [0]*len(self.__partitions))[:len(self.__partitions)]
