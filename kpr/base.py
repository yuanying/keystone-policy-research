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

import contextlib
import json
import mock
import os
import random
import string
import subprocess
import unittest

from kpr.utils import clients


def id_generator(
        size=8,
        chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
    ):
    return ''.join(random.choice(chars) for _ in range(size))


def getid(obj):
    """Return id if argument is a Resource.

    Abstracts the common pattern of allowing both an object or an object's ID
    (UUID) as a parameter when dealing with relationships.
    """
    try:
        if obj.uuid:
            return obj.uuid
    except AttributeError:  # nosec(cjschaef): 'obj' doesn't contain attribute
        # 'uuid', return attribute 'id' or the 'obj'
        pass
    try:
        return obj.id
    except AttributeError:
        return obj


class TestCase(unittest.TestCase):

    @contextlib.contextmanager
    def create_user_and_cleanup(self, project, username, role):
        user = username
        try:
            user = self.create_user(project, username, role)
            yield user
        except Exception as e:
            raise e
        finally:
            self.delete_user(project, user, role)

    def create_admin_auditor(self):
        project = self.admin.projects.find(
            name=clients.OS_ADMIN_PROJECT_NAME
        )
        username = 'admin-auditor-{}'.format(id_generator())
        return self.create_user(project, username, self.cloud_admin_auditor_role)

    def delete_admin_auditor(self, user, force=True):
        project = self.admin.projects.find(
            name=clients.OS_ADMIN_PROJECT_NAME
        )
        self.delete_user(project, user, self.cloud_admin_auditor_role, force=force)

    def create_user(self, project, username, role):
        user = self.admin.users.create(
            username,
            domain=clients.OS_USER_DOMAIN_ID,
            default_project=project,
            password=clients.OS_PASSWORD,
        )
        self.admin.roles.grant(
            role,
            user=user,
            project=project,
        )
        return user

    def delete_user(self, project, user, role, force=True):
        try:
            self.admin.roles.revoke(
                role,
                user=user,
                project=project,
            )
        except Exception as e:
            pass
        try:
            self.admin.users.delete(user)
        except Exception as e:
            if not force:
                raise e

    def os_run_text(
        self,
        command=['user', 'list'],
        project='admin',
        username='admin',
        format='json',
    ):
        args = ['openstack'] + command
        if format:
            args = args + ['-f', format]

        return subprocess.check_output(
            args,
            stderr=subprocess.STDOUT,
            env=self.get_os_env(project=project, username=username)
        )

    def os_run(
        self,
        command=['user', 'list'],
        project='admin',
        username='admin',
        format='json',
    ):
        return json.loads(self.os_run_text(
            command=command,
            project=project,
            username=username,
            format=format,
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
        self.cloud_admin_role = self.admin.roles.find(
            name='admin'
        )
        self.cloud_admin_auditor_role = self.admin.roles.find(
            name='admin_auditor'
        )
        self.project_admin_role = self.admin.roles.find(
            name='project_admin'
        )
        self.project_auditor_role = self.admin.roles.find(
            name='project_auditor'
        )
        self.project_member_role = self.admin.roles.find(
            name='Member'
        )
        self.admin_auditor = self.create_admin_auditor()

    def tearDown(self):
        super(TestCase, self).tearDown()
        self.delete_admin_auditor(self.admin_auditor)

    def setup_project(
        self,
        project='project1',
        admin=True,
        auditor=False,
        user=2
    ):
        try:
            project_name = '{}-{}'.format(project, id_generator())
            project_instance = self.admin.projects.create(
                project_name,
                clients.OS_PROJECT_DOMAIN_ID
            )
            setattr(
                self,
                project,
                project_instance
            )
        except Exception as e:
            pass

        if admin:
            self.setup_project_admin(project)
        if auditor:
            self.setup_project_auditor(project)

        self.setup_project_user(project, user)

    def get_role_by_name(self, role='admin'):
        return {
            'admin': self.project_admin_role,
            'auditor': self.project_auditor_role,
        }[role]

    def setup_project_admin_or_auditor(self, project='project1', role='admin'):
        try:
            user = '{}_{}'.format(project, role)
            user_name = '{}-{}'.format(user, id_generator())
            project_instance = getattr(self, project)
            role = self.get_role_by_name(role)

            user_instance = self.create_user(
                project_instance,
                user_name,
                role
            )
            setattr(
                self,
                user,
                user_instance
            )
        except Exception as e:
            pass

    def setup_project_admin(self, project='project1'):
        self.setup_project_admin_or_auditor(project=project, role='admin')

    def setup_project_auditor(self, project='project1'):
        self.setup_project_admin_or_auditor(project=project, role='auditor')

    def setup_project_user(self, project='project1', user=2):
        try:
            project_user = '{}_user'.format(project)
            project_instance = getattr(self, project)

            for i in range(user):
                _project_user = '{}{}'.format(project_user, i)
                _project_user_name = '{}-{}'.format(
                    _project_user, id_generator())
                _project_user_instance = self.create_user(
                    project_instance,
                    _project_user_name,
                    self.project_member_role
                )
                setattr(
                    self,
                    _project_user,
                    _project_user_instance,
                )
        except Exception as e:
            pass

    def teardown_project(
        self,
        project='project1',
        admin=True,
        auditor=False,
        user=2
    ):
        project_instance = getattr(self, project)
        if admin:
            self.teardown_project_admin(project)
        if auditor:
            self.teardown_project_auditor(project)

        self.teardown_project_user(project, user)
        try:
            self.admin.projects.delete(project_instance)
        except Exception as e:
            pass

    def teardown_project_admin_or_auditor(self, project='project1', role='admin'):
        project_instance = getattr(self, project)
        user = '{}_{}'.format(project, role)
        user = getattr(self, user)
        role = self.get_role_by_name(role)

        self.delete_user(
            project_instance,
            user,
            role,
        )

    def teardown_project_admin(self, project='project1'):
        self.teardown_project_admin_or_auditor(project=project, role='admin')

    def teardown_project_auditor(self, project='project1'):
        self.teardown_project_admin_or_auditor(project=project, role='auditor')

    def teardown_project_user(self, project='project1', user=2):
        project_instance = getattr(self, project)
        project_user = '{}_user'.format(project)

        for i in range(user):
            _project_user = '{}{}'.format(project_user, i)
            _project_user = getattr(self, _project_user)
            self.delete_user(
                project_instance,
                _project_user,
                self.project_member_role,
            )
