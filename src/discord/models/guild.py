from . import resource
from .role import Role
from .member import Member

class Guild(resource.Resource):
    
    def __init__(self, discord, **kwargs):
        super().__init__(discord, **kwargs)

        self.roles = [Role(discord, guild=self, **role) for role in self.roles]

        self.members = []

    @property
    def resource_url(self):
        return f"/guilds/{self.id}"

    def get_members_page(self, limit, after=0):
        response = self.discord.get(f"{self.resource_url}/members", params={"limit": limit, "after": after})
        json = response.json()

        return [Member(self.discord, self, **member) for member in json]

    def get_members(self):
        limit = 1000

        page = self.get_members_page(limit)
        self.members = page
        while len(page) >= limit:
            page = self.get_members_page(limit, len(page))
            self.members.extend(page)

        return self.members

    def get_role_members(self, role=None, role_id=None):
        members = []
        for member in self.members:
            if member.has_role(role=role, role_id=role_id):
                members.append(member)
        return members

    def add_member_role(self, member=None, member_id=None, role=None, role_id=None):
        member_id = member_id if member_id is not None else member.id
        role_id = role_id if role_id is not None else role.id

        response = self.discord.put(f"{self.resource_url}/members/{member_id}/roles/{role_id}")

        return response.status_code == 204

    def remove_member_role(self, member=None, member_id=None, role=None, role_id=None):
        member_id = member_id if member_id is not None else member.id
        role_id = role_id if role_id is not None else role.id

        response = self.discord.delete(f"{self.resource_url}/members/{member_id}/roles/{role_id}")

        return response.status_code == 204

    @classmethod
    def get(cls, discord, id):
        response = discord.get(f"/guilds/{id}")
        json = response.json()

        guild = cls(discord, **json)

        return guild