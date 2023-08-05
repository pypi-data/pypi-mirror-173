from typing import List, Tuple, Union

import pydantic
from typing_extensions import Literal

from classiq.interface.finance.function_input import FinanceFunctionInput
from classiq.interface.finance.model_input import FinanceModelInput, FinanceModelName
from classiq.interface.generator import function_params
from classiq.interface.generator.function_params import ParamMetadata


class Finance(function_params.FunctionParams):
    model: FinanceModelInput = pydantic.Field(description="Load a financial model")
    finance_function: Union[FinanceFunctionInput] = pydantic.Field(
        description="The finance function to solve the model"
    )

    _inputs = pydantic.PrivateAttr(default_factory=dict)
    _outputs = pydantic.PrivateAttr(default=dict.fromkeys(["out"]))

    def get_metadata(self) -> "FinanceMetadata":
        return FinanceMetadata(**self.dict())


class FinanceMetadata(ParamMetadata, Finance):
    metadata_type: Literal["finance"] = "finance"


class FinanceModelMetadata(ParamMetadata):
    metadata_type: Literal["finance_model"] = "finance_model"
    num_model_qubits: int
    distribution_range: List[float]


class FinanceModels(function_params.FunctionParams):
    model: FinanceModelInput = pydantic.Field(description="Load a financial model")

    def _create_ios(self) -> None:
        self._inputs = dict.fromkeys(["in"])
        self._outputs = dict.fromkeys(["out"])
        if self.model.name == FinanceModelName.GAUSSIAN:
            self._outputs["bernoulli_random_variables"] = None

    def get_metadata(self) -> FinanceModelMetadata:
        return FinanceModelMetadata(
            num_model_qubits=self.model.params.num_model_qubits,
            distribution_range=self.model.params.distribution_range,
        )


class FinancePayoff(function_params.FunctionParams):
    finance_function: FinanceFunctionInput = pydantic.Field(
        description="The finance function to solve the model"
    )
    num_qubits: pydantic.PositiveInt
    distribution_range: Tuple[float, float]

    _inputs = pydantic.PrivateAttr(default=dict.fromkeys(["in"]))
    _outputs = pydantic.PrivateAttr(
        default=dict.fromkeys(["out", "post_function_input"])
    )
