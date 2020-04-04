from O365.utils import ApiComponent
import logging
import json

log = logging.getLogger(__name__)

class User(ApiComponent):
    _endpoints = {
        "get": "/users/{id}",
        "invite": "",
        "create": "",
        #"activity_stats": "/users/{id}/analytics/activitystatistics"
        "activity_stats": "/me/analytics/activitystatistics",
        "recent_activity": "/me/activities/recent"

    }

    def __init__(self, *, user_id=None, parent=None, con=None, **kwargs):
        self.con = parent.con if parent else con
        protocol = parent.protocol if parent else kwargs.get("protocol")
        main_resource = parent.main_resource
        
        self.user_id = user_id
        if self.user_id is not None:
            self.get()

        super().__init__(protocol=protocol, main_resource=main_resource)

    def get(self):
        url = self.get_url(self._endpoints["get"])
        with self.con.get(url) as response:
            return response
       
    
    def get_activity_stats(self):
        url = self.get_url(self._endpoints["activity_stats"])
        with self.con.get(url) as response:
            return response
    
    def get_recent_activity(self):
        url = self.get_url(self._endpoints["recent_activity"])
        with self.con.get(url) as response:
            return response

    def create_user(self):
        pass
        
    def invite_user(self):
        pass

    def get_url(self, endpoint):
        #TO DO: add to an utility class
        url = "https://graph.microsoft.com/v1.0" + endpoint.format(id=self.user_id)
        return url