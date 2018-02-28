#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client

os_auth_url = os.environ.get('OS_AUTH_URL', 'http://172.18.11.197/identity/')
if not os_auth_url.endswith('/v3'):
    os_auth_url = "{}/v3".format(os_auth_url)

OS_AUTH_URL = os_auth_url
OS_PASSWORD = os.environ.get('OS_PASSWORD','openstack')
OS_PROJECT_DOMAIN_ID = os.environ.get('OS_PROJECT_DOMAIN_ID','default')
OS_PROJECT_NAME = os.environ.get('OS_PROJECT_NAME','admin')
OS_REGION_NAME = os.environ.get('OS_REGION_NAME','RegionOne')
OS_USERNAME = os.environ.get('OS_USERNAME','admin')
OS_USER_DOMAIN_ID = os.environ.get('OS_USER_DOMAIN_ID','default')

OS_ADMIN_PASSWORD = OS_PASSWORD
OS_ADMIN_USERNAME = OS_USERNAME
OS_ADMIN_PROJECT_NAME = OS_PROJECT_NAME

def get_admin_client():
    auth = v3.Password(
        auth_url=OS_AUTH_URL,
        username=OS_USERNAME,
        project_name=OS_PROJECT_NAME,
        password=OS_PASSWORD,
        user_domain_id=OS_USER_DOMAIN_ID,
        project_domain_id=OS_PROJECT_DOMAIN_ID,
    )
    sess = session.Session(auth=auth)
    return client.Client(session=sess)
