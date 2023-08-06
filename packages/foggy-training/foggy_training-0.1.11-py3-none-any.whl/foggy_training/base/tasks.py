from typing import List, Union

from attr import define, field


@define
class Task:
    model_inputs: Union[List[str], str] = field(converter=lambda v: v if isinstance(v, list) else [v])
    model_target: str = field()


@define
class MultiOutputRegression(Task):
    pass


@define
class Classification(Task):
    pass


@define
class TransformerTask(Task):
    tokenize_column: str = field()
