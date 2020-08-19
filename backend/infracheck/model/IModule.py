import inspect
from abc import abstractmethod, ABC
from typing import Any, Dict

from infracheck.model.IParam import IParam


class IModule(ABC):
    """ A Test module is a single test inside a test set """

    @property
    @abstractmethod
    def documentation(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def id(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def version(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def params(self) -> Dict[str, IParam]:
        raise NotImplementedError

    @property
    def code(self):
        """
        Returns the source code
        :return:
        """
        return inspect.getsource(self.test)

    @abstractmethod
    def test(self) -> Any:
        """
        This should be implemented for each module individually
        :return:
        """
        raise NotImplementedError

    def set_module_data(self, data: Dict[str, Any]):
        """
        Takes input data formatted like
        {
            field_1: data_for_field_1,
            field_2: data_for_field_2
        }
        and passes them to the module
        :param data:
        :return:
        """
        for key in self.params.keys():
            self.params[key]['value'] = data[key]
