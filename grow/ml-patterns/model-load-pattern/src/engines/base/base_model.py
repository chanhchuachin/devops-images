import traceback
from abc import ABC, abstractmethod
from functools import wraps


class MLModel(ABC):
    """Base class for ML model prediction code."""

    def __init__(self, *args, **kwargs) -> None:
        """Create an MLModel instance by adding any deserialization and initialization code for the model."""
        self.__checkpoint_status = False
        self.__checkpoint_version = None

    def __repr__(self):
        """Return a string representing the model object."""
        return self.__class__.__name__

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Abstract property that returns a display name for the model.
        Returns:
            str: The display name of the model.

        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def model_instance(self) -> str:
        """Abstract property that returns the instace name of the model when initialized.
        Returns:
            str: The qualified name of the model.

        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def description(self) -> str:
        """Abstract property that returns a description of the model.
        Returns:
            str: The description of the model.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def metadata(self) -> dict[str]:
        """Abstract property that returns a metada of the model.
        Returns:
            str: The medadata of the model.
        """
        raise NotImplementedError()

    @property
    def checkpoint_version(self) -> str:
        """Method that return version of model!
        Returns:
            str: The version of the model.
        """
        return self.__checkpoint_version

    @checkpoint_version.setter
    def checkpoint_version(self, version):
        self.__checkpoint_version = version

    @property
    def checkpoint_status(self) -> bool:
        """Method that return status when loading the model success or not!
        Returns:
            str: The checkpoint status of model instance.
        """
        return self.__checkpoint_status

    @checkpoint_status.setter
    def checkpoint_status(self, status: bool) -> bool:
        if status is True:
            self.__checkpoint_status = status

    @abstractmethod
    def checkpoint_dir(self) -> str:
        """Abstract property that returns a directory contain checkpoint.
        Returns:
            str: The abstract file path of the checkpoint dir.
        """
        raise NotImplementedError()

    @abstractmethod
    def load_checkpoint(self) -> None:
        """Abstract method use to load model checkpoint."""
        raise NotImplementedError()

    @abstractmethod
    def predict(self, *args, **kwargs):
        """Prediction with the model.
        Args:
            args, kwargs: parameters used by the model for making a prediction
        Returns:
            object: can be any python type
        """
        raise NotImplementedError()

    def update_checkpoint_status(load_checkpoint_func: load_checkpoint):
        """
        The decorator function helper update checkpoint status of load_checkpoint function
        """
        wraps(load_checkpoint_func)

        def wrap(self):
            try:
                load_checkpoint_func(self)
                self.checkpoint_status = True
            except Exception as exc:
                message = f"{self}-{load_checkpoint_func.__name__} error due to {exc}!"
                print(message)

        return wrap


class MLModelException(Exception):
    """Exception base class used to raise exceptions within MLModel derived classes."""

    def __init__(self, *args):
        """Initialize MLModelException instance."""
        Exception.__init__(self, *args)
