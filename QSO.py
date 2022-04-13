import time
import requests


def fetch_next_task():
    return requests.get('http://127.0.0.1:5000/next_task')


# Might rename this execute
def parse_task(task):
    print("PARSE")
    # First : _id
    # Second: task_id
    # Third: task_type
    # Fourth + = extra
    for key in task:
        if key not in ["_id", "task_id", "task_type"]:
            print(f"{key}: {task[key]}")


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
        time.sleep(10)


if __name__ == '__main__':
    beacon_loop()
