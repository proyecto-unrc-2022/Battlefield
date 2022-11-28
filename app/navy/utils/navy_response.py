class NavyResponse:
    def __init__(self, status=None, message=None, data=None):
        self.status = status
        self.message = message
        self.data = data

    def to_json(self):
        return {"status": self.status, "message": self.message, "data": self.data}

    def __str__(self):
        return str(self.to_json())

    def __repr__(self):
        return str(self.to_json())
