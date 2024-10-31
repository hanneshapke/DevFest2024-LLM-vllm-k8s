from typing import List
from typing import Dict, List, Union
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


ENDPOINT_ID = ""
PROJECT_ID = ""

PROMPT = """
<start_of_turn>user
You are a helpful AI assistant excellent in writing poetry.
Please write a Haiku about the amazing DevFest Silicon Valley and Responsible AI
<end_of_turn>
<start_of_turn>model
"""


def predict(
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    instances = instances if isinstance(instances, list) else [instances]
    instances = [json_format.ParseDict(instance_dict, Value()) for instance_dict in instances]

    endpoint = client.endpoint_path(project=project, location=location, endpoint=endpoint_id)
    response = client.predict(endpoint=endpoint, instances=instances, timeout=50000.0)
    return response.predictions


if __name__ == "__main__":
    instances = [{
      "prompt": PROMPT,
      "max_tokens": 256
    }]
    rs = predict(PROJECT_ID, ENDPOINT_ID, instances)
    print(rs)



