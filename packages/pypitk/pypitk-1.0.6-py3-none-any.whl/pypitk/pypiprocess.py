from .pydantic_model import PydanticModel, Field
from . import constants as _constants


class PYPIProcess(PydanticModel):

    config_path: str = Field("")
    task: str = Field("")
    open_in_finder: bool = Field(False)
    open_in_vscode: bool = Field(False)
