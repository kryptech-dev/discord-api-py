from . import resource

class Role(resource.Resource):

    def __init__(self, discord, guild=None, **kwargs):
        super().__init__(discord, **kwargs)

        self.guild = guild

    @property
    def resource_url(self):
        return f"{self.guild.resource_url}/roles/{self.id}"