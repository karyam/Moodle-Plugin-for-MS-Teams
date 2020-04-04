from O365.utils import ApiComponent
import logging
import json

log = logging.getLogger(__name__)


class Group(ApiComponent):
    _endpoints = {
        "create": "/groups",  # POST
        "get": "/groups/{id}",  # GET
        "update": "/groups/{id}",  # PATCH
        "delete": "/groups/{id}",  # DELETE
        "list": "/groups",  # GET
        "renew": "/groups/{id}/renew",  # POST
        "add_owner": "/groups/{id}/owners/$ref",  # POST
        "list_owners": "/groups/{id}/owners",  # GET
        "remove_owner": "/groups/{id}/owners/{id}/$ref",  # DELETE
        "add_member": "/groups/{id}/members/$ref",  # POST
        "remove_member": "/groups/{id}/members/{id}/$ref",  # DELETE
        "user": "/users/",
        "reports": "/reports/getTeamsUserActivityCounts(period='D7')"
    }

    _teams_endpoints = {
        "create": "/groups/{id}/team",  # PUT
        "get": "/teams/{id}",  # GET
        "list_members": "/groups/{id}/members",  # GET
        #"get_members": "/groups/{id}/members",
        "reports": "/reports/getTeamsUserActivityCounts(period='D7')",
        "update": "/teams/{id}",  # PATCH
        "delete": "/groups/{id}",  # DELETE
        "clone": "/teams/{id}/clone",  # POST
        "archive": "/teams/{id}/archive",  # POST
        "unarchive": "/teams/{id}/unarchive",  # POST
        "adminList": "/users/{id}/joinedTeams",  # POST
        # "listAllTeams" : "/teams/{group-id}", #GET
        "add_app": "/teams/{id}/installedApps",  # POST
        "add_channel": "/teams/{id}/channels/",  # POST
        "list_channel_messages": "GET /teams/{id}/channels/{id}/messages",
        "add_member": "/groups/{id}/members/$ref" #POST
        
    }

    def __init__(self, *, group_id=None, parent=None, con=None, **kwargs):
        self.con = parent.con if parent else con
        protocol = parent.protocol if parent else kwargs.get("protocol")
        main_resource = parent.main_resource
        self.group_id = group_id
        self.current_group_data = None
        self.team_id = None
        self.listed_team_data = [None]*16
        self.current_team_data = None
        if self.group_id is not None:
            self.get()

        super().__init__(protocol=protocol, main_resource=main_resource)

    def create(self, display_name: str, mail_enabled: bool, 
               security_enabled: bool, owners,
               members, description=None,
               mail_nickname=None):
        url = self.generate_url(self._endpoints["create"])
        data = {
            "description": description,
            "displayName": display_name,
            "groupTypes": ["Unified"],
            "mailEnabled": mail_enabled,
            "mailNickname": mail_nickname,
            "securityEnabled": security_enabled
        }
        memberURL = self.generate_url(self._endpoints["user"])

        if owners is not None:
            owner_data = [memberURL + user_id for user_id in owners]
            data["owners@odata.bind"] = owner_data
        if members is not None:
            member_data = [memberURL + user_id for user_id in members]
            data["members@odata.bind"] = member_data
        with self.con.post(url, data=data) as response:
            self.group_id = json.loads(response.text)["id"]
            return response

    def get(self):
        url = self.generate_url(self._endpoints["get"])
        with self.con.get(url) as response:
            return response

    def update(self, display_name: bool = None, mail_enabled: bool = None, security_enabled: bool = None) -> None:
        i = 0
        data = {}
        lables = ["displayName", "mailEnabled", "securityEnabled"]
        for change in [display_name, mail_enabled, security_enabled]:
            if change is not None:
                data[lables[i]] = change
            i += 1

        url = self.generate_url(self._endpoints["update"])
        self.con.patch(url, data)

    def delete(self):
        url = self.generate_url(self._endpoints["delete"])
        self.set_id(None)
        self.con.delete(url)
    
    def team_list_channel_messages(self, channel_id=None):
        pass
    
    def get_reports(self):
        url = self.generate_url(self._endpoints["reports"])
        with self.con.get(url) as response:
            return response



    def create_team(self, allowCreateUpdateChannels=False, allowDeleteChannels=False, allowAddRemoveApps=False,
                    allowCreateUpdateRemoveTabs=False, allowCreateUpdateRemoveConnectors=False,
                    allowGuestCreateUpdateChannels=False, allowGuestDeleteChannels=False, allowUserEditMessages=True,
                    allowUserDeleteMessages=True, allowOwnerDeleteMessages=True, allowTeamMentions=True,
                    allowChannelMentions=True,
                    allowGiphy=True, giphyContentRating="strict", allowStickersAndMemes=True, allowCustomMemes=True):

        url = self.generate_url(self._teams_endpoints["create"])
        
        self.listed_team_data = [allowCreateUpdateChannels, allowDeleteChannels, allowAddRemoveApps,
                                 allowCreateUpdateRemoveTabs, allowCreateUpdateRemoveConnectors,
                                 allowGuestCreateUpdateChannels,
                                 allowGuestDeleteChannels, allowUserEditMessages, allowUserDeleteMessages,
                                 allowOwnerDeleteMessages, allowTeamMentions, allowChannelMentions, allowGiphy,
                                 giphyContentRating,
                                 allowStickersAndMemes, allowCustomMemes]

        data = self.generate_teams_json()

        with self.con.put(url, data) as response:
            self.current_team_data = data
            # is it ok for the team to have the same id as its corresponding group
            self.team_id = self.group_id
            return response

        

    def delete_team(self):
        url = self.generate_url(self._teams_endpoints["delete"])
        with self.con.delete(url) as response:
            self.current_team_data = None
            self.team_id = None
            return response

    def get_team(self, id=None):
        url = self.generate_url(self._teams_endpoints["get"], id)
        with self.con.get(url) as response:
            self.current_team_data = json.loads(response.text)
            self.update_team_from_json(self.current_team_data)
            return response

    def get_members(self):
        url = self.generate_url(self._teams_endpoints["list_members"])
        with self.con.get(url) as response:

            return response

    def generate_teams_json(self):
        data = {
            "memberSettings": {
                "allowCreateUpdateChannels": self.listed_team_data[0],
                "allowDeleteChannels": self.listed_team_data[1],
                "allowAddRemoveApps": self.listed_team_data[2],
                "allowCreateUpdateRemoveTabs": self.listed_team_data[3],
                "allowCreateUpdateRemoveConnectors": self.listed_team_data[4]
            },
            "guestSettings": {
                "allowCreateUpdateChannels": self.listed_team_data[5],
                "allowDeleteChannels": self.listed_team_data[6]
            },
            "messagingSettings": {
                "allowUserEditMessages": self.listed_team_data[7],
                "allowUserDeleteMessages": self.listed_team_data[8],
                "allowOwnerDeleteMessages": self.listed_team_data[9],
                "allowTeamMentions": self.listed_team_data[10],
                "allowChannelMentions": self.listed_team_data[11]
            },
            "funSettings": {
                "allowGiphy": self.listed_team_data[12],
                "giphyContentRating": self.listed_team_data[13],
                "allowStickersAndMemes": self.listed_team_data[14],
                "allowCustomMemes": self.listed_team_data[15]
            }
        }

        return data

    def update_team_from_json(self, jsondata):
        i = 0
        updateableParameters = ["memberSettings", "guestSettings", "messagingSettings", "funSettings"]
        for parameter in updateableParameters:
            for _, value in jsondata[parameter].items():
                self.listed_team_data[i] = value
                i+=1


    def update_team(self, allowCreateUpdateChannels=None, allowDeleteChannels=None, allowAddRemoveApps=None,
                    allowCreateUpdateRemoveTabs=None, allowCreateUpdateRemoveConnectors=None,
                    allowGuestCreateUpdateChannels=None, allowGuestDeleteChannels=None, allowUserEditMessages=None,
                    allowUserDeleteMessages=None, allowOwnerDeleteMessages=None, allowTeamMentions=None,
                    allowChannelMentions=None,
                    allowGiphy=None, giphyContentRating=None, allowStickersAndMemes=None, allowCustomMemes=None):

        i=0
        for parameter in [allowCreateUpdateChannels, allowDeleteChannels, allowAddRemoveApps,
                                 allowCreateUpdateRemoveTabs, allowCreateUpdateRemoveConnectors,
                                 allowGuestCreateUpdateChannels,
                                 allowGuestDeleteChannels, allowUserEditMessages, allowUserDeleteMessages,
                                 allowOwnerDeleteMessages, allowTeamMentions, allowChannelMentions, allowGiphy,
                                 giphyContentRating,
                                 allowStickersAndMemes, allowCustomMemes]:
            if parameter is not None:
                self.listed_team_data[i] = parameter
            i+=1

        data = self.generate_teams_json()
        url = self.generate_url(self._teams_endpoints["update"])
        
        with self.con.patch(url, data) as response:
            self.get_team()
            return response


    # To be used later
    # def createTeam(self, teamType: str, channels=None, allowCreateUpdateChannels=False,
    #                allowDeleteChannels=False, allowAddRemoveApps=False, allowCreateUpdateRemoveTabs=False,
    #                allowCreateUpdateRemoveConnectors=False):
    #     """Team type can be "standard", "educationClass" or "educationStaff"""
    #     url = "https://graph.microsoft.com/beta/teamsTemplates('{}')"
    #     microsoftGraphBetaAPIURL = "https://graph.microsoft.com/beta/teams"
    #     if teamType == "standard":
    #         url.format("standard")
    #     elif teamType == "educationClass":
    #         url.format("educationClass")
    #     elif teamType == "educationStaff":
    #         url.format("educationStaff")
    #     else:
    #         raise ValueError("Team can be \"standard\", \"educationClass\" or \"educationStaff\"")
    #
    #     data = {}
    #     channeldata = []
    #     data["template@odata.bind"] = url
    #     data["group@odata.bind"] = "https://graph.microsoft.com/v1.0/groups('{}')".format(self.group_id)
    #     for channel in channels:
    #         channeldata.append({"displayName": channel[0], "isFavoriteByDefault": channel[1]})
    #     data["memberSettings"] = {
    #         "allowCreateUpdateChannels": allowCreateUpdateChannels,
    #         "allowDeleteChannels": allowDeleteChannels,
    #         "allowAddRemoveApps": allowAddRemoveApps,
    #         "allowCreateUpdateRemoveTabs": allowCreateUpdateRemoveTabs,
    #         "allowCreateUpdateRemoveConnectors": allowCreateUpdateRemoveConnectors
    #     }
    #     with self.con.post(microsoftGraphBetaAPIURL, data) as response:
    #         return response

    
    def add_channel(self):
        url = self.generate_url(self._teams_endpoints["add_channel"])
        channel_data = {"displayName": "General Channel", "description": "This is the main channel for the class."}
        with self.con.post(url, data=channel_data) as response:
            return response
    
    def archive_team(self):
        url = self.generate_url(self._teams_endpoints["archive"])
        with self.con.post(url) as response:
            return response

    def unarchive_team(self):
        url = self.generate_url(self._teams_endpoints["unarchive"])
        with self.con.post(url) as response:
            return response


    def get_id(self):
        return self.group_id

    def set_id(self, id):
        self.group_id = id

    def generate_url(self, endpoint):
        url = "https://graph.microsoft.com/v1.0" + endpoint.format(id=self.group_id)
        return url
