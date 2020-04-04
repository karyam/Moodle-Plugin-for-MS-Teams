from O365.utils import ApiComponent
import logging
import json

log = logging.getLogger(__name__)


def class Team(ApiComponent):

    _endpoints = {
        "get": "/teams/{id}",
        "get_members": "/groups/{id}/members",
        "get_channels": "/teams/id/channels",
        "get_channel_info": ""
    }
    
    def __init__(self, *, id=None, parent=None, con=None, **kwargs):
        self.con = parent.con if parent else con
        protocol = parent.protocol if parent else kwargs.get("protocol")
       
        main_resource = parent.main_resource
       
        self._id = id
        self.listed_team_data = [None]*16
        self.current_team_data = None
        
        if self._id is not None:
            self.get()

        super().__init__(protocol=protocol, main_resource=main_resource)
    
    def get(self):
        url = self.get_url(self._endpoint["get"])
        with self.con.get(url) as response:
            return response
    
    def get_id(self):
        return self._id

    def get_members(self):
        url = self.get_url(self._endpoints["get_members"])
        with self.con.get(url) as response:
            return response

    def get_channels(self):
        pass
         

    def team_channels(self):
        pass

    def generate_url(self):
        url = "https://graph.microsoft.com/v1.0" + endpoint.format(id=self._id)
        return url
    
    def generate_url_beta(self):
        url = "https://graph.microsoft.com/beta" + endpoint.format(id=self._id)
        return url
