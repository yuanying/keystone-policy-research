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

import json
import mock
import os
import subprocess
import unittest

from kpr.utils import clients


class TestCase(unittest.TestCase):

    def os_run_text(
        self, command=['user', 'list'], project='admin', username='admin'):
        args = ['openstack'] + command + ['-f', 'json']
        return subprocess.check_output(
            args,
            stderr=subprocess.STDOUT,
            env=self.get_os_env(project=project, username=username)
        )

    def os_run(self, command=['user', 'list'], project='admin', username='admin'):
        return json.loads(self.os_run_text(
            command=command,
            project=project,
            username=username
        ).decode('utf-8'))

    def get_os_env(self, project='admin', username='admin'):
        return {
            'OS_AUTH_URL': clients.OS_AUTH_URL,
            'OS_IDENTITY_API_VERSION': '3',
            'OS_NO_CACHE': '1',
            'OS_PASSWORD': clients.OS_PASSWORD,
            'OS_PROJECT_DOMAIN_ID': clients.OS_PROJECT_DOMAIN_ID,
            'OS_PROJECT_NAME': project,
            'OS_REGION_NAME': clients.OS_REGION_NAME,
            'OS_USERNAME': username,
            'OS_USER_DOMAIN_ID': clients.OS_USER_DOMAIN_ID,
            'OS_VOLUME_API_VERSION': '2',
            'PATH': os.environ['PATH'],
        }

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
                clients.OS_PROJECT_DOMAIN_ID
            )
            setattr(
                self,
                project,
                project_instance
            )
            project_admin_instance = self.admin.users.create(
                project_admin,
                domain=clients.OS_USER_DOMAIN_ID,
                default_project=project_instance,
                password=clients.OS_PASSWORD,
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
                    domain=clients.OS_USER_DOMAIN_ID,
                    default_project=project_instance,
                    password=clients.OS_PASSWORD,
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
            raise e

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
            except Exception as e:
                pass
            try:
                self.admin.roles.revoke(
                    self.project_member_role,
                    user=_project_user,
                    project=project,
                )
            except Exception as e:
                pass
            try:
                self.admin.users.delete(_project_user)
            except Exception as e:
                pass

        try:
            self.admin.projects.delete(project)
        except Exception as e:
            pass
