from . import resource
from . import user

class Member(resource.Resource):

    def __init__(self, discord, guild, **kwargs):
        super().__init__(discord, kwargs["user"]["id"], **kwargs)

        self.guild = guild
        self.user = user.User(discord, **self.user)

    def has_role(self, role=None, role_id=None):
        if role is not None:
            role_id = role.id
        if role_id is not None:
            return role_id in self.roles
