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

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client


def get_admin_client():
    auth = v3.Password(
        auth_url="http://172.18.11.197/identity/v3",
        username="admin",
        project_name="admin",
        password="openstack",
        user_domain_id="default",
        project_domain_id="default",
    )
    sess = session.Session(auth=auth)
    return client.Client(session=sess)


def get_client(project, username):
    auth = v3.Password(
        auth_url="http://172.18.11.197/identity/v3",
        username=username,
        project_name=project,
        password="openstack",
        user_domain_id="default",
        project_domain_id="default",
    )
    sess = session.Session(auth=auth)
    return client.Client(session=sess)
