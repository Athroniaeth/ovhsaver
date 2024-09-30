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
        """Return a fake server"""
        return FakeServer(id=id, status=self.status)

    def start_server(self, id: int):
        """Start a fake server"""
        ...

    def stop_server(self, id: int):
        """Stop a fake server"""
        ...

    def shelve_server(self, id: int):
        """Shelve a fake server"""
        ...

    def unshelve_server(self, id: int):
        """Unshelve a fake server"""
        ...

    def suspend_server(self, server: FakeServer):
        """Stop a fake server"""
        ...

    def wait_for_server(self, server: FakeServer, status="ACTIVE", failures=["ERROR"], interval=60, wait=360):
        """Wait for a fake server to be in a specific status"""
        ...


class FakeConnection:
    def __init__(self, status="ACTIVE"):
        self.compute = FakeCompute(status=status)
