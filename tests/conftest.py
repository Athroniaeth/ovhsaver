class FakeServer:
    id: int
    name: str = "fake-server"
    status: str

    def __init__(self, id: int, status: str):
        self.id = id
        self.status = status


class FakeCompute:
    def __init__(self, status="ACTIVE"):
        self.status = status

    def get_server(self, id: int):
        return FakeServer(id=id, status=self.status)

    def start_server(self, id: int):
        ...

    def stop_server(self, server: FakeServer):
        ...

    def wait_for_server(self, server: FakeServer, status="ACTIVE", failures=["ERROR"], interval=60, wait=360):
        ...


class FakeConnection:
    def __init__(self, status="ACTIVE"):
        self.compute = FakeCompute(status=status)
