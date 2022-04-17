from . import resource

class User(resource.Resource):

    def __init__(self, discord, **kwargs):
        super().__init__(discord, **kwargs)