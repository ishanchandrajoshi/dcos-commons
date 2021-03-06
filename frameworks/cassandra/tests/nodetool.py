from typing import List, Tuple

import sdk_cmd


def cmd(service_name: str, task_name: str, command: str) -> Tuple[int, str, str]:
    return sdk_cmd.service_task_exec(
        service_name,
        task_name,
        "bash -c 'JAVA_HOME=$(ls -d jdk*/) apache-cassandra-*/bin/nodetool {}'".format(command),
    )


def parse_status(output: str) -> List['Node']:
    nodes = []
    for line in _get_status_lines(output):
        node = _parse_status_line(line)
        nodes.append(node)

    return nodes


def _get_status_lines(output: str) -> List[str]:
    raw_lines = output.splitlines()[5:]
    lines = []
    for raw_line in raw_lines:
        if raw_line.strip() != "":
            lines.append(raw_line)

    return lines


def _parse_status_line(line: str) -> 'Node':
    # Input looks like this:
    # UN  10.0.2.28   74.32 KB   256          62.8%             d71b5d8d-6db1-416e-a25d-4541f06b26bc  us-west-2c

    elements = line.split()

    status = elements[0]
    address = elements[1]
    load_size = elements[2]
    load_unit = elements[3]
    tokens = elements[4]
    owns = elements[5]
    host_id = elements[6]
    rack = elements[7]

    # Fix up the load tokens
    load = load_size + " " + load_unit

    return Node(status, address, load, tokens, owns, host_id, rack)


class Node(object):
    def __init__(
        self,
        status: str,
        address: str,
        load: str,
        tokens: str,
        owns: str,
        host_id: str,
        rack: str,
    ) -> None:
        self.status = status
        self.address = address
        self.load = load
        self.tokens = tokens
        self.owns = owns
        self.host_id = host_id
        self.rack = rack

    def __str__(self) -> str:
        return "status: {}, address: {}, load: {}, tokens: {}, owns: {}, host_id: {}, rack: {}".format(
            self.status, self.address, self.load, self.tokens, self.owns, self.host_id, self.rack
        )

    def get_status(self) -> str:
        return self.status

    def get_address(self) -> str:
        return self.address

    def get_load(self) -> str:
        return self.load

    def get_tokens(self) -> str:
        return self.tokens

    def get_owns(self) -> str:
        return self.owns

    def get_host_id(self) -> str:
        return self.host_id

    def get_rack(self) -> str:
        return self.rack
