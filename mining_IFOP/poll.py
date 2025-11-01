# coding: utf-8

import abc
from typing import List

class CandidatePollInterface(abc.ABC):
    @abc.abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_scores(self) -> List[str]:
        raise NotImplementedError
