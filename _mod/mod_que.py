import json
from google.cloud import tasks_v2


def mz_que(que_project, que_location, que_id, que_url, que_body):
    # task client
    client = tasks_v2.CloudTasksClient()

    # queue name
    parent = client.queue_path(que_project, que_location, que_id)

    # create task
    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": que_url,
            "headers": {"Content-type": "application/json"},
            "body": json.dumps(que_body).encode(),
        }
    }

    # task execute
    # client.create_task(parent=parent, task=task)
    request = {"parent": parent, "task": task}
    client.create_task(request=request)

    return
