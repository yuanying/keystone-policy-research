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

import mock
import unittest

from kpr.utils import clients


class TestCase(unittest.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.addCleanup(mock.patch.stopall)
        self.admin = clients.get_admin_client()
        self.project_admin_role = self.admin.roles.find(
            name='project_admin'
        )

    def setup_project(self, project='project1'):
        project_admin = '{}_admin'.format(project)
        project_user = '{}_user'.format(project)

        setattr(
            self,
            project,
            self.admin.projects.create(
                project,
                'default'
            )
        )
        setattr(
            self,
            project_admin,
            self.admin.users.create(
                project_admin,
                domain='default',
                default_project=getattr(self, project),
                password='openstack',
            )
        )
        self.admin.roles.grant(
            self.project_admin_role,
            user=getattr(self, project_admin),
            project=getattr(self, project)
        )
        setattr(
            self,
            project_user,
            self.admin.users.create(
                project_user,
                domain='default',
                default_project=getattr(self, project),
                password='openstack',
            )
        )

    def teardown_project(self, project='project1'):
        project_admin = '{}_admin'.format(project)
        project_admin = getattr(self, project_admin)
        project_user = '{}_user'.format(project)
        project_user = getattr(self, project_user)
        project = getattr(self, project)

        self.admin.roles.revoke(
            self.project_admin_role,
            user=project_admin,
            project=project,
        )
        self.admin.users.delete(project_admin)
        self.admin.users.delete(project_user)
        self.admin.projects.delete(project)
