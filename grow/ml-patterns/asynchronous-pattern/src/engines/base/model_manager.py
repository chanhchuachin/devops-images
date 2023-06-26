import importlib
from typing import List

from src.engines.base.base_model import MLModel


class ModelManager(object):
    """Singleton class that instantiates and manages model objects."""

    def __new__(cls):
        """Create and return a new ModelManager instance, after instance is first created it will always be returned."""
        if not hasattr(cls, "_instance"):
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance._is_initialized = False
        return cls._instance

    def __init__(self):
        """Construct ModelManager object."""
        if self._is_initialized is False:
            self._models = []
            self._is_initialized = True

    @classmethod
    def clear_instance(cls):
        """Clear singleton instance from class."""
        del cls._instance

    def load_model(self, class_path: str) -> None:
        """Import and instantiate an MLModel object from a class path.
        Args:
            class_path: Class path to the model's MLModel class.
        Raises:
            ValueError: Raised if the model is not a subtype of MLModel, or if a model with the same qualified name
                      is already loaded in the ModelManager.
        """

        try:
            module_path = ".".join(class_path.split(".")[:-1])
            class_name = class_path.split(".")[-1]

            # importing the model class
            model_module = importlib.import_module(module_path)
            model_class = getattr(model_module, class_name)

            # instantiating the model object from the class
            model_object = model_class()

            self.add_model(model_object, class_path)
        except Exception as exc:
            print(f"load {class_path} fail due to {exc}")

    def add_model(self, model: MLModel, class_path: str = None) -> None:
        """Add a model to the ModelManager.
        Args:
            model: instance of MLModel
        """
        if not isinstance(model, MLModel):
            raise ValueError(
                "ModelManager instance can only hold references to objects of type MLModel."
            )

        if model.model_instance in [model.model_instance for model in self._models]:
            raise ValueError(
                "A model with the same qualified name is already in the ModelManager singleton."
            )

        if class_path is not None:
            model.class_path = class_path
        else:
            model.class_path = None

        self._models.append(model)

    def remove_model(self, model_instance: str) -> None:
        """Remove an MLModel object from the ModelManager singleton.
        Args:
            model_instance: The qualified name of the model to be returned.
        Raises:
            ValueError: Raised if a model with the qualified name can't be found in the ModelManager singleton.
        """
        # searching the list of model objects to find the one with the right qualified name
        model = next(
            (model for model in self._models if model.model_instance == model_instance),
            None,
        )

        if model is None:
            raise ValueError(
                "Instance of model '{}' not found in ModelManager.".format(
                    model_instance
                )
            )
        else:
            self._models.remove(model)

    def get_models(self) -> List[dict]:
        """
        Get a list of models in the model manager singleton.
        Returns:
            List of dictionaries containing information about the model instances in the ModelManager singleton.
        """
        model_objects = [
            {
                "display_name": model.display_name,
                "model_instance": model.model_instance,
                "description": model.description,
                "checkpoint_version": model.checkpoint_version,
                "checkpoint_status": model.checkpoint_status,
                "class_path": model.class_path,
            }
            for model in self._models
        ]
        return model_objects

    def get_model_metadata(self, model_instance: str) -> dict:
        """
        Get model metadata by qualified name.
        Args:
            model_instance: Qualified name of the model for which to get metadata
        Returns:
            Dictionary containing information about a model in the ModelManager singleton.

        """
        # searching the list of model objects to find the one with the right qualified name
        model = next(
            (model for model in self._models if model.model_instance == model_instance),
            None,
        )

        if model is None:
            raise ValueError(
                "Instance of model '{}' not found in ModelManager.".format(
                    model_instance
                )
            )
        else:
            return {
                "display_name": model.display_name,
                "model_instance": model.model_instance,
                "description": model.description,
                "version": model.version,
            }

    def get_model(self, model_instance: str) -> MLModel:
        """Get a model object by qualified name.
        Args:
            model_instance: The qualified name of the model to be returned.
        Returns:
            Model object
        Raises:
            ValueError: Raised if a model with the qualified name can't be found in the ModelManager singleton.
        """
        # searching the list of model objects to find the one with the right qualified name
        model = next(
            (model for model in self._models if model.model_instance == model_instance),
            None,
        )

        if model is None:
            raise ValueError(
                "Instance of model '{}' not found in ModelManager.".format(
                    model_instance
                )
            )
        else:
            return model
