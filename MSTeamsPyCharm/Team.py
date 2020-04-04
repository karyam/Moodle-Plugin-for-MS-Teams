from O365.utils import ApiComponent


class Team(ApiComponent):
    _endpoints = {
        "create": "/groups/{id}/team",  # PUT
        "get": "/teams/{id}",  # GET
        "update": "/teams/{id}",  # PATCH
        "delete": "/groups/{id}",  # DELETE
        "clone": "/teams/{id}/clone",  # POST
        "archive": "/teams/{id}/archive",  # POST
        "unarchive": "/teams/{id}/unarchive",  # POST
        "adminList": "/users/{id}/joinedTeams",  # POST
        # "listAllTeams" : "/teams/{group-id}", #GET
        "add_app": "/teams/{id}/installedApps",  # POST
        "add_channel": "/teams/{id}/channels/{id}/tabs"  # POST
    }

    def __init__(self, *, team_id=None, parent=None, con=None, **kwargs):
        self.con = parent.con if parent else con
        protocol = parent.protocol if parent else kwargs.get("protocol")
        main_resource = parent.main_resource
        self.team_id = team_id
        super().__init__(protocol=protocol, main_resource=main_resource)

    def get_team(self):
        url = self.generate_url(self._endpoints["get"])
        with self.con.get(url) as response:
            return response



    def update_team(self):
        url = self.generate_url(self._endpoints["update"])


    def get_id(self):
        return self.team_id

    def set_id(self, id):
        self.team_id = id

    def generate_url(self, endpoint):
        url = "https://graph.microsoft.com/v1.0" + endpoint.format(id=self.team_id)
        return url
