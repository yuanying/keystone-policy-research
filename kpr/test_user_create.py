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
import subprocess

from kpr import base
from kpr.utils import clients


class TestUserCreate(base.TestCase):

    def setUp(self):
        super(TestUserCreate, self).setUp()
        self.setup_project('project1', user=1)
        self.setup_project('project2', admin=False, user=0)

    def tearDown(self):
        super(TestUserCreate, self).tearDown()
        self.teardown_project('project1', user=1)
        self.teardown_project('project2', admin=False, user=0)

    @contextlib.contextmanager
    def create_user_by_cli(
        self,
        project,
        username,
        role,
        run_user,
        run_user_project,
    ):
        output = { "id": "" }
        project_id = base.getid(project)
        role_name = role.name
        try:
            output = self.os_run(
                project=run_user_project.name,
                username=run_user.name,
                command=[
                    'user',
                    'create',
                    username,
                    '--domain',
                    clients.OS_USER_DOMAIN_ID,
                    '--project',
                    project_id,
                    '--password',
                    'password'
                ],
            )
            self.os_run_text(
                project=run_user_project.name,
                username=run_user.name,
                format=None,
                command=[
                    'role',
                    'add',
                    '--user',
                    output['id'],
                    '--project',
                    project_id,
                    role_name,
                ],
            )
            yield output
        except Exception as e:
            raise e
        finally:
            self.delete_user(
                project,
                output['id'],
                role,
            )

    # Project1 テナント管理者は Project1 に属するユーザを作成することができる。
    def test_create_project1_user_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        with self.create_user_by_cli(
            self.project1,
            testuser,
            self.project_member_role,
            self.project1_admin,
            self.project1,
        ) as output:
            self.assertEqual(testuser, output['name'])

    # Project1 テナント管理者は Project2 に属するユーザを作成することができない。
    def test_create_project2_user_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        try:
            with self.create_user_by_cli(
                self.project2,
                testuser,
                self.project_member_role,
                self.project1_admin,
                self.project1,
            ) as output:
                self.fail("project admin must not be permitted to create user")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # Project1 テナント管理者は Project1 に属するテナント管理者を作成することができる。
    def test_create_project1_admin_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        with self.create_user_by_cli(
            self.project1,
            testuser,
            self.project_admin_role,
            self.project1_admin,
            self.project1,
        ) as output:
            self.assertEqual(testuser, output['name'])

    # Project1 テナント管理者は Project2 に属するテナント管理者を作成することができない。
    def test_create_project2_admin_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        try:
            with self.create_user_by_cli(
                self.project2,
                testuser,
                self.project_admin_role,
                self.project1_admin,
                self.project1,
            ) as output:
                self.fail("project admin must not be permitted to create user")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # Project1 テナント管理者は Project2 で認証した場合、Project1 に属するユーザを作成することができない。
    def test_create_project1_user_by_project_admin_user_with_project1_creds(self):
        pass

    # Project1 テナントユーザは Project1 に属するユーザを作成することができない。
    def test_create_project1_user_by_project1_user(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        try:
            with self.create_user_by_cli(
                self.project1,
                testuser,
                self.project_member_role,
                self.project1_user0,
                self.project1,
            ) as output:
                self.fail("project user must not be permitted to create user")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # Project1 テナントユーザは Project2 に属するユーザを作成することができない。
    def test_create_project1_user_by_project1_user(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        try:
            with self.create_user_by_cli(
                self.project2,
                testuser,
                self.project_member_role,
                self.project1_user0,
                self.project1,
            ) as output:
                self.fail("project user must not be permitted to create user")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')
