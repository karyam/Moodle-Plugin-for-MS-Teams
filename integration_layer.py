from requests_oauthlib import OAuth2Session
import os
import time
import yaml
import json
import O365
from O365 import Account, MSGraphProtocol, Connection
from MSTeamsPyCharm.Group import Group
from MSTeamsPyCharm.User import User
from MSTeamsPyCharm.Team import Team
import python3_gearman
import simplejson
import sys


def init_auth():
    client_secret = "W9hAa7i62Uv?hLTLH-?BlxhRCYWIkj?A"
    application_id = "bdf4dd0c-9ba0-4bc2-b72f-d7ce5023f0b9"
    credentials = (application_id, client_secret)
    tenant_id = "17855ce0-d47e-48df-9c90-33b4fa21c861"
    account = Account(credentials, auth_flow_type="credentials", tenant_id=tenant_id)
    account.authenticate()
    return account

    
def create_team(gearman_worker, gearman_job):
    data = simplejson.loads(gearman_job.data)
    maria_user_id = "d3f30d7a-d742-46ee-b41a-c127a2eeca6a"
    louis_user_id = "92ced39c-df19-4ae6-b370-59a118b0e767"
    developer_id = "e95e11ac-4423-4bfd-813d-d7fb38b28e3c"
    
    members_list = []
    if data[3] is False:
        members_list = [maria_user_id, louis_user_id]
    else: 
        csv = data[3].split(',')
        for x in csv:
            if "-" in x:
                members_list.append(x)
        members_list = members_list[0:10]
    
    client_secret = "W9hAa7i62Uv?hLTLH-?BlxhRCYWIkj?A"
    application_id = "bdf4dd0c-9ba0-4bc2-b72f-d7ce5023f0b9"
    credentials = (application_id, client_secret)
    tenant_id = "17855ce0-d47e-48df-9c90-33b4fa21c861"
    account = Account(credentials, auth_flow_type="credentials", tenant_id=tenant_id)
    
    new_group = Group(parent=account, protocol=MSGraphProtocol())
    new_group.create(data[0], mail_enabled=True, security_enabled=True, owners=[developer_id],
                    members=members_list, description=data[1])

    new_group.create_team(True, True, True, True, True, True, True, True, True, True, True, True, True, "strict", True,
                         True)

    # send the team is for later database storage
    return new_group.team_id

def archive_nd_delete_team(gearman_worker, gearman_job):
    client_secret = "W9hAa7i62Uv?hLTLH-?BlxhRCYWIkj?A"
    application_id = "bdf4dd0c-9ba0-4bc2-b72f-d7ce5023f0b9"
    credentials = (application_id, client_secret)
    tenant_id = "17855ce0-d47e-48df-9c90-33b4fa21c861"
    account = Account(credentials, auth_flow_type="credentials", tenant_id=tenant_id)

    team_id = simplejson.loads(gearman_job.data)
    
    print(team_id)
    
    group = Group(group_id=team_id, parent=account, protocol=MSGraphProtocol())
    group.archive_team()
    
    #group.delete_team()
    print("The team was deleted!")
    group.delete()
    return "Requested team was deleted successfully!"

def update_team(gearman_worker, gearman_job):
    
    client_secret = "W9hAa7i62Uv?hLTLH-?BlxhRCYWIkj?A"
    application_id = "bdf4dd0c-9ba0-4bc2-b72f-d7ce5023f0b9"
    credentials = (application_id, client_secret)
    tenant_id = "17855ce0-d47e-48df-9c90-33b4fa21c861"
    account = Account(credentials, auth_flow_type="credentials", tenant_id=tenant_id)

    data = simplejson.loads(gearman_job.data)
    
    team_id = str(data[0])
    new_name = str(data[1])

    print(team_id, new_name)

    group = Group(group_id=team_id, parent=account, protocol=MSGraphProtocol())
    group.update(display_name=new_name, mail_enabled=True, security_enabled=True)
    
    print("Group id: " + group.team_id)
    return group.team_id
    #return "Team was renamed!"




def analytics():
    client_secret = "W9hAa7i62Uv?hLTLH-?BlxhRCYWIkj?A"
    application_id = "bdf4dd0c-9ba0-4bc2-b72f-d7ce5023f0b9"
    credentials = (application_id, client_secret)
    tenant_id = "17855ce0-d47e-48df-9c90-33b4fa21c861"
    # scopes = ['https://graph.microsoft.com/beta/Analytics.Read', 
    #           'https://graph.microsoft.com/beta/Analytics.ReadWrite', 
    #           'https://graph.microsoft.com/beta/Analytics.Read.All',
    #           'https://graph.microsoft.com/beta/Analytics.ReadWrite.All']
    account = Account(credentials, auth_flow_type="credentials", tenant_id=tenant_id)

    user = User(user_id="d3f30d7a-d742-46ee-b41a-c127a2eeca6a", parent=account, protocol=MSGraphProtocol())
    print(user.get_recent_activity())

def get_team_data(team_id="955529db-5622-4dca-9c90-8cb0e5fe032f"):
    client_secret = "W9hAa7i62Uv?hLTLH-?BlxhRCYWIkj?A"
    application_id = "bdf4dd0c-9ba0-4bc2-b72f-d7ce5023f0b9"
    credentials = (application_id, client_secret)
    tenant_id = "17855ce0-d47e-48df-9c90-33b4fa21c861"
    account = Account(credentials, auth_flow_type="credentials", tenant_id=tenant_id)
    account.authenticate()
    
    team = Group(group_id=team_id, parent=account, protocol=MSGraphProtocol())
    
    print(team.get_id())
    response = team.get_reports()
    print(json.loads(response.text))
    with open('data.txt', 'w') as outfile:
        json.dump(response.text, outfile)

gm_worker = python3_gearman.GearmanWorker(['localhost:4730'])

while(True):
    print("Waiting for client requests...")
    gm_worker.register_task('create_team', create_team)
    gm_worker.register_task('update_team', update_team)
    gm_worker.register_task('archive_nd_delete_team', archive_nd_delete_team)
    gm_worker.work()
