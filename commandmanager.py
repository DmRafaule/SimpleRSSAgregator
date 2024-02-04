class CommandManager():
    _instance = None
    _map = {}

    def __new__(self):
        if self._instance is None:
            self._instance = super(CommandManager, self).__new__(self)
        return self._instance

    def set(self, func_id: str, func):
        self._map[func_id] = func

    def get(self, func_id: str):
        return self._map[func_id]
