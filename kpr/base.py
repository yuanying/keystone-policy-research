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
        self.project_member_role = self.admin.roles.find(
            name='Member'
        )

    def setup_project(self, project='project1'):
        try:
            project_admin = '{}_admin'.format(project)
            project_user = '{}_user'.format(project)

            project_instance = self.admin.projects.create(
                project,
                'default'
            )
            setattr(
                self,
                project,
                project_instance
            )
            project_admin_instance = self.admin.users.create(
                project_admin,
                domain='default',
                default_project=project_instance,
                password='openstack',
            )
            setattr(
                self,
                project_admin,
                project_admin_instance
            )
            self.admin.roles.grant(
                self.project_admin_role,
                user=project_admin_instance,
                project=project_instance
            )
            for i in (0, 1):
                _project_user = '{}{}'.format(project_user, i)
                _project_user_instance = self.admin.users.create(
                    _project_user,
                    domain='default',
                    default_project=getattr(self, project),
                    password='openstack',
                )
                setattr(
                    self,
                    _project_user,
                    _project_user_instance,
                )
            self.admin.roles.grant(
                self.project_member_role,
                user=_project_user_instance,
                project=project_instance
            )
        except Exception as e:
            pass

    def teardown_project(self, project='project1'):
        project_user = '{}_user'.format(project)
        project_admin = '{}_admin'.format(project)
        # project_admin = getattr(self, project_admin)
        try:
            project_admin = self.admin.users.find(name=project_admin)
        except Exception as e:
            pass

        # project = getattr(self, project)
        try:
            project = self.admin.projects.find(name=project)
        except Exception as e:
            raise

        try:
            self.admin.roles.revoke(
                self.project_admin_role,
                user=project_admin,
                project=project,
            )
        except Exception as e:
            pass

        try:
            self.admin.users.delete(project_admin)
        except Exception as e:
            pass


        for i in (0, 1):
            _project_user = '{}{}'.format(project_user, i)
            # _project_user = getattr(self, _project_user)
            try:
                _project_user = self.admin.users.find(name=_project_user)
                self.admin.roles.revoke(
                    self.project_member_role,
                    user=_project_user,
                    project=project,
                )
                self.admin.users.delete(_project_user)
            except Exception as e:
                pass

        try:
            self.admin.projects.delete(project)
        except Exception as e:
            pass
