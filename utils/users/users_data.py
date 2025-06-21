class UsersData:
    def __init__(
        self,
            data=None
    ) -> None:
        if data is None:
            data = {}
        self.messages_data = data.get("messages_data", {})
        self.connection_data = data.get("connection_data", {})

    def to_dict(self):
        return {
            "messages_data": self.messages_data,
            "connection_data": self.connection_data
        }
