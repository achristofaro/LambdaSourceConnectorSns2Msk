class Message:
  
    def __init__(self, data: dict):
        self.data = data
    
    def validate(self):
        if not isinstance(self.data, dict):
            raise ValueError('Message must be a dictionary')

    @classmethod
    def from_json(cls, json_data):
        return cls(data=json_data)

    def to_json(self):
        return {'data': self.data}

    def __str__(self):
        return self.__dict__.__str__()