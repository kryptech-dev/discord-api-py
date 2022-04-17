class Resource():

    def __init__(self, discord, id, **kwargs):
        self.discord = discord
        self.id = id

        self.from_dict(kwargs)

    def from_dict(self, d):
        for key, value in d.items():
            setattr(self, key, value)