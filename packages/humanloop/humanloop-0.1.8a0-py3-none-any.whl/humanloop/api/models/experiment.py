import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from .metric import BaseMetricResponse
from .model_config import ModelEndpoint, ModelProvider
from .utils import KeyValues


class TrialResponse(BaseModel):
    """A trial contains information about a sampled model configuration, and
    additionally includes an ID for a follow-up log."""

    id: str = Field(
        title="Trial ID",
        description="Unique ID of trial to reference in subsequent log calls.",
    )
    model_config_id: str = Field(
        title="Model config ID",
        description="Unique ID of the model config associated to the trial.",
    )
    experiment_id: str = Field(
        title="Experiment",
        description="Unique ID of the experiment the trial belongs to.",
    )
    model_config_name: Optional[str] = Field(
        title="Model config name",
    )
    model: str = Field(
        title="Instance of model used",
        description="What instance of model was used for the generation?"
        "e.g. text-davinci-002. ",
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
        " configuration on Humanloop. For example, the temperature setting.",
    )
    provider: Optional[ModelProvider] = Field(
        title="Model provider",
        description="The company who is hosting the target model.",
    )
    endpoint: Optional[ModelEndpoint] = Field(
        title="Provider endpoint",
        description="Which of the providers model endpoints to use."
        "For example Complete or Edit. ",
    )


class ExperimentModelConfigResponse(BaseModel):
    mean: Optional[float] = Field(
        title="Mean of experiment's metric",
        description="The mean performance of the model config, as measured by the experiment's metric.",
    )
    spread: Optional[float] = Field(
        title="Spread of experiment's metric",
        description="The spread of performance of the model config, as measured by the experiment's metric. "
        "A measure of the uncertainty in the model config's performance.",
    )
    trials_count: int = Field(
        title="The number of trials that have happened in this experiment",
        description="Number of datapoints with feedback associated to this experiment.",
    )
    active: bool = Field(
        title="Model config active",
        description="Whether the model config is active in the experiment. "
        "Only active model configs can be sampled from the experiment.",
    )
    id: str = Field(
        title="Model config ID",
        description="String ID of model config. Starts with `config_`.",
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
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PositiveLabel(BaseModel):
    group: str = Field(title="Feedback group", description="Name of feedback group")
    label: str = Field(title="Feedback label", description="Name of feedback label")


class ExperimentStatus(str, Enum):
    initialised = "Initialized"
    in_progress = "In progress"


class ExperimentResponse(BaseModel):
    id: str = Field(
        title="Experiment ID",
        description="String ID of experiment. Starts with `exp_`.",
    )
    project_id: str = Field(
        title="Project ID",
        description="String ID of project the experiment belongs to. Starts with `pr_`.",
    )
    name: str = Field(title="Experiment name", description="Name of experiment.")

    status: ExperimentStatus = Field(
        title="Experiment status", description="Status of experiment."
    )
    model_configs: Optional[List[ExperimentModelConfigResponse]] = Field(
        title="Experiment model configs",
        description="List of model configs associated to the experiment.",
    )
    metric: BaseMetricResponse = Field(
        title="Experiment metric",
        description="Metric used as the experiment's objective.",
    )
    positive_labels: List[PositiveLabel] = Field(
        title="Positive labels",
        description="Feedback labels to treat as positive user feedback. "
        "Used to monitor the performance of model configs in the experiment.",
    )
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CreateExperimentRequest(BaseModel):
    name: str = Field(title="Experiment name", description="Name of experiment.")
    model_config_ids: Optional[List[str]] = Field(
        title="Model config IDs",
        description="Model configs to add to this experiment. Further model configs can be added later.",
    )
    positive_labels: List[PositiveLabel] = Field(
        title="Positive labels",
        description="Feedback labels to treat as positive user feedback. "
        "Used to monitor the performance of model configs in the experiment.",
    )
    set_active: bool = Field(
        default=False,
        title="Set as project's active experiment",
        description="Whether to set the created project as the project's active experiment.",
    )


class UpdateExperimentRequest(BaseModel):
    name: Optional[str] = Field(
        title="Experiment name", description="Name of experiment."
    )
    positive_labels: Optional[List[PositiveLabel]] = Field(
        title="Positive labels",
        description="Feedback labels to treat as positive user feedback. "
        "Used to monitor the performance of model configs in the experiment.",
    )
    config_ids_to_register: Optional[List[str]] = Field(
        title="Model config IDs to register",
        description="Model configs to add to this experiment.",
    )
    config_ids_to_deregister: Optional[List[str]] = Field(
        title="Model config IDs to deregister",
        description="Model configs in this experiment to be deactivated.",
    )
