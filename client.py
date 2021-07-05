import click
import requests
from requests.exceptions import ConnectionError


@click.command()
@click.option("--host", default="localhost", help="Server address(default=localhost)")
@click.option("--port", default="5000", help="Server port(default=5000)")
@click.option("--action", default="", help="CREATE to create task and GET to get status or result")
@click.option("--type", default="", help="REVERSE or REPLACE")
@click.option("--text", default="", help="text of yor task")
@click.option("--id", default="", help="task id")
def main(host, port, action, type, text, id):
    if action == "CREATE":
        create_task(host, port, type, text)
    elif action == "GET":
        get_data(host, port, id)


def create_task(host, port, type_, text):
    try:
        req = requests.post(f"http://{host}:{port}/tasks", json={"type": type_, "text": text})
        if req.status_code != 200:
            print(req.json())
        else:
            print(req.content)
    except ConnectionError:
        print("invalid address")


def get_data(host, port, id_):
    print(requests.get(f"http://{host}:{port}/tasks/{id_}").content.decode())


if __name__ == '__main__':
    main()
