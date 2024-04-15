import copy
from abc import abstractmethod
from typing import Any

from agogos._core import _Block, _SequentialSystem, _ParallelSystem, _Base


class TransformType(_Base):
    """Abstract transform type describing a class that implements the transform function"""

    @abstractmethod
    def transform(self, data: Any, **transform_args: Any) -> Any:
        """Transform the input data.

        :param data: The input data.
        :param transform_args: Keyword arguments.
        :return: The transformed data."""
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement transform method."
        )


class Transformer(TransformType, _Block):
    """The transformer block transforms any data it could be x or y data.

    Methods:
    .. code-block:: python
        @abstractmethod
        def transform(self, data: Any, **transform_args: Any) -> Any:
            # Transform the input data.

        def get_hash(self) -> str:
            # Get the hash of the Transformer

        def get_parent(self) -> Any:
            # Get the parent of the Transformer

        def get_children(self) -> list[Any]:
            # Get the children of the Transformer

        def save_to_html(self, file_path: Path) -> None:
            # Save html format to file_path

    Usage:
    .. code-block:: python
        from agogos.transformer import Transformer

        class MyTransformer(Transformer):
            def transform(self, data: Any, **transform_args: Any) -> Any:
                # Transform the input data.
                return data

        my_transformer = MyTransformer()
        transformed_data = my_transformer.transform(data)
    """


class TransformingSystem(TransformType, _SequentialSystem):
    """A system that transforms the input data.

    Parameters:
    - steps (list[Transformer | TransformingSystem | ParallelTransformingSystem]): The steps in the system.

    Implements the following methods:
    .. code-block:: python
        def transform(self, data: Any, **transform_args: Any) -> Any:
            # Transform the input data.

        def get_hash(self) -> str:
            # Get the hash of the TransformingSystem

        def get_parent(self) -> Any:
            # Get the parent of the TransformingSystem

        def get_children(self) -> list[Any]:
            # Get the children of the TransformingSystem

        def save_to_html(self, file_path: Path) -> None:
            # Save html format to file_path


    Usage:
    .. code-block:: python
        from agogos.transforming_system import TransformingSystem

        transformer_1 = CustomTransformer()
        transformer_2 = CustomTransformer()

        transforming_system = TransformingSystem(steps=[transformer_1, transformer_2])
        transformed_data = transforming_system.transform(data)
        predictions = transforming_system.predict(data)
    """

    def __post_init__(self) -> None:
        """Post init method for the TransformingSystem class."""

        # Assert all steps are a subclass of Transformer
        for step in self.steps:
            if not isinstance(step, (TransformType)):
                raise TypeError(f"{step} is not an instance of TransformType")

        super().__post_init__()

    def transform(self, data: Any, **transform_args: Any) -> Any:
        """Transform the input data.

        :param data: The input data.
        :return: The transformed data.
        """

        # Loop through each step and call the transform method
        for step in self.steps:
            step_name = step.__class__.__name__

            step_args = transform_args.get(step_name, {})
            if isinstance(step, (TransformType)):
                data = step.transform(data, **step_args)
            else:
                raise TypeError(f"{step} is not an instance of TransformType")

        return data


class ParallelTransformingSystem(TransformType, _ParallelSystem):
    """A system that transforms the input data in parallel.

    Parameters:
    - steps (list[Transformer | TransformingSystem | ParallelTransformingSystem]): The steps in the system.

    Methods:
    .. code-block:: python
        @abstractmethod
        def concat(self, original_data: Any), data_to_concat: Any, weight: float = 1.0) -> Any:
            # Specifies how to concat data after parallel computations

        def get_hash(self) -> str:
            # Get the hash of the ParallelTransformingSystem.

        def get_parent(self) -> Any:
            # Get the parent of the ParallelTransformingSystem.

        def get_children(self) -> list[Any]:
            # Get the children of the ParallelTransformingSystem

        def save_to_html(self, file_path: Path) -> None:
            # Save html format to file_path

    Usage:
    .. code-block:: python
        from agogos.parallel_transforming_system import ParallelTransformingSystem

        transformer_1 = CustomTransformer()
        transformer_2 = CustomTransformer()

        class CustomParallelTransformingSystem(ParallelTransformingSystem):
            def concat(self, data1: Any, data2: Any) -> Any:
                # Concatenate the transformed data.
                return data1 + data2

        transforming_system = CustomParallelTransformingSystem(steps=[transformer_1, transformer_2])

        transformed_data = transforming_system.transform(data)
    """

    def __post_init__(self) -> None:
        """Post init method for the ParallelTransformingSystem class."""

        # Assert all steps are a subclass of Transformer or TransformingSystem
        for step in self.steps:
            if not isinstance(step, (TransformType)):
                raise TypeError(f"{step} is not an instance of TransformType")

        # Sort the steps by name, to ensure consistent ordering of parallel computations
        self.steps = sorted(self.steps, key=lambda x: x.__class__.__name__)

        super().__post_init__()

    def transform(self, data: Any, **transform_args: Any) -> Any:
        """Transform the input data.

        :param data: The input data.
        :return: The transformed data.
        """
        # Loop through each step and call the transform method
        num_steps = len(self.get_steps())
        out_data = None
        if len(self.get_steps()) == 0:
            return data

        for i, step in enumerate(self.get_steps()):
            step_name = step.__class__.__name__

            step_args = transform_args.get(step_name, {})

            if isinstance(step, (TransformType)):
                step_data = step.transform(copy.deepcopy(data), **step_args)
                out_data = self.concat(out_data, step_data, 1 / num_steps)
            else:
                raise TypeError(f"{step} is not an instance of TransformType")

        return out_data
