import uuid

from google.cloud import aiplatform
from typing import Dict, Optional, Sequence
from google.cloud.aiplatform import explain

def upload_model(
    project: str,
    display_name: str,
    serving_container_image_uri: str,
    model_id: Optional[str] = None,
    version_description: Optional[str] = None,
    parent_model: Optional[str] = None,
    is_default_version: bool = False,
    location: str = None,
    artifact_uri: Optional[str] = None,
    serving_container_predict_route: Optional[str] = None,
    serving_container_health_route: Optional[str] = None,
    description: Optional[str] = None,
    serving_container_command: Optional[Sequence[str]] = None,
    serving_container_args: Optional[Sequence[str]] = None,
    serving_container_environment_variables: Optional[Dict[str, str]] = None,
    serving_container_ports: Optional[Sequence[int]] = None,
    instance_schema_uri: Optional[str] = None,
    parameters_schema_uri: Optional[str] = None,
    prediction_schema_uri: Optional[str] = None,
    explanation_metadata: Optional[explain.ExplanationMetadata] = None,
    explanation_parameters: Optional[explain.ExplanationParameters] = None,
    sync: bool = True,
    labels: Optional[Dict[str, str]] = None,
):
    """Upload a model to Google Cloud Vertex AI Model Registry."""

    aiplatform.init(project=project, location=location)

    if not parent_model:
        is_default_version = True

    model = aiplatform.Model.upload(
        display_name=display_name,
        artifact_uri=artifact_uri,
        model_id=model_id,
        version_description=version_description,
        parent_model=parent_model,
        is_default_version=is_default_version,
        serving_container_image_uri=serving_container_image_uri,
        serving_container_predict_route=serving_container_predict_route,
        serving_container_health_route=serving_container_health_route,
        instance_schema_uri=instance_schema_uri,
        parameters_schema_uri=parameters_schema_uri,
        prediction_schema_uri=prediction_schema_uri,
        description=description,
        serving_container_command=serving_container_command,
        serving_container_args=serving_container_args,
        serving_container_environment_variables=serving_container_environment_variables,
        serving_container_ports=serving_container_ports,
        explanation_metadata=explanation_metadata,
        explanation_parameters=explanation_parameters,
        sync=sync,
        labels=labels,
    )

    model.wait()

    print(f"Model {model.display_name} is ready and registered.")
    print(f"Model resource name: {model.resource_name}")
    return model

def create_endpoint(
    project: str,
    display_name: str,
    location: str = None,
):
    """Create a Google Cloud Vertex AI Endpoint."""

    aiplatform.init(project=project, location=location)

    endpoint = aiplatform.Endpoint.create(
        display_name=display_name,
    )

    print(f"Endpoint {endpoint.display_name} is created.")
    print(f"Endpoint resource name: {endpoint.resource_name}")
    return endpoint

def deploy_model(
    project: str,
    model: str,
    endpoint: str,
    display_name: str,
    traffic_split: Dict[str, float],
    location: str = None,
    machine_type: Optional[str] = None,
    accelerator_type: Optional[str] = None,
    accelerator_count: Optional[int] = None,
):
    """Deploy a model to Google Cloud Vertex AI Endpoint."""

    aiplatform.init(project=project, location=location)

    model = aiplatform.Model(model)
    endpoint = aiplatform.Endpoint(endpoint)

    deployed_model = endpoint.deploy(
        model=model,
        deployed_model_display_name=display_name,
        traffic_split=traffic_split,
        machine_type=machine_type,
        accelerator_type=accelerator_type,
        accelerator_count=accelerator_count,
    )

    print(f"Model {model.display_name} is deployed to endpoint {endpoint.display_name}.")
    print(f"Deployed model resource name: {deployed_model}")
    return deployed_model

# main
if __name__ == "__main__":

    project = "..."
    display_name = "gemma2-2b-it"
    model_id = "gemma2-2b-it"
    version_description = str(uuid.uuid4())
    parent_model = "gemma2-2b-it"
    is_default_version = True
    serving_container_image_uri = "us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20241030_0916_RC00"
    serving_container_predict_route = "/generate"
    serving_container_health_route = "/health"
    description = "vLLM model for generating text"
    serving_container_command = [
      "python3", "-m", "vllm.entrypoints.api_server"]
    serving_container_args = [
        "--model=google/gemma-2-2b-it",
        "--tensor-parallel-size=1",
        "--max-model-len=4096",
    ]
    serving_container_ports = [8000]
    serving_container_environment_variables = {
      "HUGGING_FACE_HUB_TOKEN": "..."}
    sync=True
    machine_type="g2-standard-8"
    accelerator_type="NVIDIA_L4"
    accelerator_count=1

    model = upload_model(
        project=project,
        display_name=display_name,
        model_id=model_id,
        version_description=version_description,
        parent_model=parent_model,
        is_default_version=is_default_version,
        serving_container_image_uri=serving_container_image_uri,
        serving_container_predict_route=serving_container_predict_route,
        serving_container_health_route=serving_container_health_route,
        description=description,
        serving_container_command=serving_container_command,
        serving_container_args=serving_container_args,
        serving_container_environment_variables=serving_container_environment_variables,
        serving_container_ports=serving_container_ports,
        sync=sync,
    )
    print(f"Completed uploading model {model.display_name}")

    endpoint = create_endpoint(
        project=project,
        display_name=display_name,
    )
    print(f"Completed creating endpoint {endpoint.display_name}")

    deployed_model = deploy_model(
        project=project,
        model=model.resource_name,
        endpoint=endpoint.resource_name,
        display_name=display_name,
        traffic_split={"0": 100},
        machine_type=machine_type,
        accelerator_type=accelerator_type,
        accelerator_count=accelerator_count,
    )

    print("Completed deploying model to endpoint")
