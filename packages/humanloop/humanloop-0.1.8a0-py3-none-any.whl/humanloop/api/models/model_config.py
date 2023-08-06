import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .utils import KeyValues


class ModelProvider(str, Enum):
    """Supported model providers."""

    openai = "OpenAI"
    mock = "Mock"


class ModelEndpoint(str, Enum):
    """Supported model provider endpoints."""

    complete = "Complete"
    edit = "Edit"


class ModelConfig(BaseModel):
    name: Optional[str] = Field(
        title="Config name",
        description="A friendly display name for config. If not provided a name "
        "will be generated.",
    )
    project: str = Field(
        title="Project name",
        description="Unique project name. If it does not exist, a new project will "
        "be created.",
    )
    experiment: Optional[str] = Field(
        title="Experiment tag",
        description="Include a model configuration in an experiment group. "
        "Experiment groups are used for A/B testing and optimizing "
        "hyperparameters.",
    )
    model: str = Field(
        title="Type of model used",
        description="What model type was used for the generation? e.g. text-davinci-002. ",
    )
    prompt_template: Optional[str] = Field(
        title="Prompt template",
        description="Prompt template that incorporated your specified inputs to form "
        "your final request to the model.",
    )
    parameters: Optional[KeyValues] = Field(
        title="Model parameters",
        description="The hyperparameter settings that along with your model source "
        "and prompt template (if provided) will uniquely determine a model"
        " configuration on Humanloop. For example the temperature setting.",
    )
    provider: Optional[ModelProvider] = Field(
        title="Model provider",
        description="The company who is hosting the target model.",
        default=ModelProvider.openai,
    )
    endpoint: Optional[ModelEndpoint] = Field(
        title="Provider endpoint",
        description="Which of the providers model endpoints to use. "
        "For example Complete or Edit. ",
        default=ModelEndpoint.complete,
    )


class ModelConfigResponse(BaseModel):
    id: str = Field(
        title="Model config ID",
        description="String ID of model config. Starts with `config_`.",
    )
    project_id: Optional[str] = Field(
        title="Project ID",
        description="String ID of project the model config belongs to. Starts with `pr_`.",
    )
    display_name: str = Field(
        title="Display name",
        description="Display name of model config. If this is not set by the user, a friendly name will be generated.",
    )
    model_name: str = Field(
        title="Name of language model",
        description="Model used for generation. E.g. text-davinci-002.",
    )
    prompt_template: Optional[str] = Field(
        title="Prompt template",
        description="Prompt template that incorporated your specified inputs to form "
        "your final request to the model.",
    )
    parameters: Optional[dict] = Field(
        title="Model parameters",
        description="Provider specific hyper-parameter settings "
        "that along with your model and prompt template (if provided) "
        "will uniquely determine a model configuration on Humanloop. "
        "For example, the temperature setting.",
    )
    provider: Optional[ModelProvider] = Field(
        title="Model provider",
        description="The organization hosting the target model.",
    )
    endpoint: Optional[ModelEndpoint] = Field(
        title="Provider endpoint",
        description="Which of the providers' endpoints to use. E.g. Complete, Edit.",
    )
    experiment_id: Optional[str] = Field(
        title="Experiment ID",
        description="The ID of the experiment the model config has been registered to. "
        "Only populated when registering a model config to an experiment.",
    )
    created_at: datetime.datetime


class GetModelConfigResponse(ModelConfigResponse):
    """A selected model configuration.

    If the model configuration was selected in the context of an experiment,
    the response will include a trial_id to associate a subsequent log() call.
    """

    trial_id: Optional[str] = Field(
        title="Trial ID",
        description="ID of trial to reference in subsequent log calls.",
    )
