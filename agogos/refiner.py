from dataclasses import dataclass
import numpy as np

from abc import abstractmethod

from agogos._core.block import Block


@dataclass
class Refiner(Block):

    @abstractmethod
    def predict(self, predictions: np.ndarray) -> np.ndarray:
        """Predict the target variable.
        
        :param predictions: The predictions to refine.
        :return: The predictions."""
        raise NotImplementedError