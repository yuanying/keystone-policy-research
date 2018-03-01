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


class TestUserDelete(base.TestCase):

    def setUp(self):
        super(TestUserDelete, self).setUp()
        self.setup_project('project1')
        self.setup_project('project2')

    def tearDown(self):
        super(TestUserDelete, self).tearDown()
        self.teardown_project('project1')
        self.teardown_project('project2')

    def delete_user_by_cli(
        self,
        project,
        user,
        role,
        run_user,
        run_user_project,
    ):
        user_id = base.getid(user)
        project_id = base.getid(project)
        role_name = role.name

        self.os_run_text(
            project=run_user_project.name,
            username=run_user.name,
            format=None,
            command=[
                'role',
                'remove',
                '--user',
                user_id,
                '--project',
                project_id,
                role_name,
            ],
        )

        self.os_run_text(
            project=run_user_project.name,
            username=run_user.name,
            format=None,
            command=[
                'user',
                'delete',
                user_id,
            ],
        )

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

    # Project1 テナント管理者は Project1 に属するユーザを削除することができる。
    def test_delete_project1_user_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        with self.create_user_and_cleanup(
            self.project1,
            testuser,
            self.project_member_role,
        ) as user:
            self.delete_user_by_cli(
                self.project1,
                user,
                self.project_member_role,
                self.project1_admin,
                self.project1,
            )

    # Project1 テナント管理者は Project2 に属するユーザを削除することができない。
    def test_delete_project2_user_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        try:
            with self.create_user_and_cleanup(
                self.project2,
                testuser,
                self.project_member_role,
            ) as user:
                self.delete_user_by_cli(
                    self.project2,
                    user,
                    self.project_member_role,
                    self.project1_admin,
                    self.project1,
                )
                self.failed("project admin must not be permitted to delete user")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # Project1 テナント管理者は Project1 に属するテナント管理者を削除することができる。
    def test_delete_project1_admin_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        with self.create_user_and_cleanup(
            self.project1,
            testuser,
            self.project_admin_role,
        ) as user:
            self.delete_user_by_cli(
                self.project1,
                user,
                self.project_admin_role,
                self.project1_admin,
                self.project1,
            )

    # Project1 テナント管理者は Project2 に属するテナント管理者を削除することができない。
    def test_delete_project2_admin_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        try:
            with self.create_user_and_cleanup(
                self.project2,
                testuser,
                self.project_admin_role,
            ) as user:
                self.delete_user_by_cli(
                    self.project2,
                    user,
                    self.project_admin_role,
                    self.project1_admin,
                    self.project1,
                )
                self.failed("project admin must not be permitted to delete user")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # Project1 テナント管理者は Project2 で認証した場合、Project1 に属するユーザを削除することができない。
    def test_delete_project1_user_by_project_admin_user_with_project1_creds(self):
        pass

    # Project1 テナントユーザは Project1 に属するユーザを削除することができない。
    def test_delete_project1_user_by_project1_user(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        try:
            with self.create_user_and_cleanup(
                self.project1,
                testuser,
                self.project_member_role,
            ) as user:
                self.delete_user_by_cli(
                    self.project1,
                    user,
                    self.project_member_role,
                    self.project1_user0,
                    self.project1,
                )
                self.failed("project admin must not be permitted to delete user")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # Project1 テナントユーザは Project2 に属するユーザを削除することができない。
    def test_delete_project1_user_by_project1_user(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        try:
            with self.create_user_and_cleanup(
                self.project2,
                testuser,
                self.project_member_role,
            ) as user:
                self.delete_user_by_cli(
                    self.project2,
                    user,
                    self.project_member_role,
                    self.project1_user0,
                    self.project1,
                )
                self.failed("project admin must not be permitted to delete user")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')
