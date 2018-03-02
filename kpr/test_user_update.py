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

import subprocess

from kpr import base
from kpr.utils import clients


class TestUserUpdate(base.TestCase):

    def setUp(self):
        super(TestUserUpdate, self).setUp()
        self.setup_project('project1', user=1)
        self.setup_project('project2', admin=False, user=0)

    def tearDown(self):
        super(TestUserUpdate, self).tearDown()
        self.teardown_project('project1', user=1)
        self.teardown_project('project2', admin=False, user=0)

    def update_user(
        self,
        target_user,
        run_user=None,
        run_user_project=None,
        command=["--email", 'test@example.com'],
        update_project=False,
    ):
        command = ['user', 'set'] + command
        if not update_project:
            command = command + ['--project', target_user.default_project_id]

        command = command + [target_user.id]
        self.os_run_text(
            project=run_user_project.name,
            username=run_user.name,
            format=None,
            command=command
        )

    # クラウド管理者は Project1 に属するユーザのプロジェクトを変更することができる。
    def test_update_project1_user_default_project_by_cloud_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        with self.create_user_and_cleanup(
            self.project1,
            testuser,
            self.project_member_role,
        ) as user:
            self.admin.users.update(user, default_project=self.project2)
            user = self.admin.users.get(user)
            self.assertEqual(user.default_project_id, self.project2.id)

    # Project1 テナント管理者は Project1 に属するユーザのメールアドレスを変更することができる。
    def test_update_project1_user_email_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())
        expected_email_address = "{}@example.com".format(testuser)

        with self.create_user_and_cleanup(
            self.project1,
            testuser,
            self.project_member_role,
        ) as user:
            self.update_user(
                user,
                run_user=self.project1_admin,
                run_user_project=self.project1,
                command=['--email', expected_email_address],
            )
            user = self.admin.users.get(user)
            self.assertEqual(user.email, expected_email_address)

    # Project1 テナント管理者は Project1 に属するユーザのパスワードを変更することができる。
    def test_update_project1_user_password_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())
        expected_password = testuser

        try:
            with self.create_user_and_cleanup(
                self.project1,
                testuser,
                self.project_member_role,
            ) as user:
                self.update_user(
                    user,
                    run_user=self.project1_admin,
                    run_user_project=self.project1,
                    command=['--password', expected_password],
                )
        except subprocess.CalledProcessError as e:
            self.failed("Failed to update password by project1_admin")

    # Project1 テナント管理者は Project1 に属するユーザのプロジェクトを変更することができない。
    def test_update_project1_user_default_project_by_project1_admin(self):
        testuser = 'testuser-{}'.format(base.id_generator())

        try:
            with self.create_user_and_cleanup(
                self.project1,
                testuser,
                self.project_member_role,
            ) as user:
                self.update_user(
                    user,
                    run_user=self.project1_admin,
                    run_user_project=self.project1,
                    command=['--project', self.project2.id],
                    update_project=True,
                )
                self.failed("project admin must not be permitted to update user's project")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # Project1 テナントユーザは Project2 に属するユーザのメールアドレスを変更することができない。
    def test_update_project1_user_email_by_project2_user(self):
        testuser = 'testuser-{}'.format(base.id_generator())
        expected_email_address = "{}@example.com".format(testuser)

        try:
            with self.create_user_and_cleanup(
                self.project2,
                testuser,
                self.project_member_role,
            ) as user:
                self.update_user(
                    user,
                    run_user=self.project1_admin,
                    run_user_project=self.project1,
                    command=['--email', expected_email_address],
                )
                self.failed("project admin must not be permitted to update user's email")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # Project1 テナントユーザは Project2 に属するユーザのパスワードを変更することができない。
    def test_update_project1_user_password_by_project2_user(self):
        testuser = 'testuser-{}'.format(base.id_generator())
        expected_password = "{}@example.com".format(testuser)

        try:
            with self.create_user_and_cleanup(
                self.project2,
                testuser,
                self.project_member_role,
            ) as user:
                self.update_user(
                    user,
                    run_user=self.project1_admin,
                    run_user_project=self.project1,
                    command=['--password', expected_password],
                )
                self.failed("project admin must not be permitted to update user's password")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # Project1 テナントユーザは Project1 に属するユーザのメールアドレスを変更することができない。
    def test_update_project1_user_default_project_by_project1_user(self):
        testuser = 'testuser-{}'.format(base.id_generator())
        expected_email_address = "{}@example.com".format(testuser)

        try:
            with self.create_user_and_cleanup(
                self.project1,
                testuser,
                self.project_member_role,
            ) as user:
                self.update_user(
                    user,
                    run_user=self.project1_user0,
                    run_user_project=self.project1,
                    command=['--email', expected_email_address],
                )
                self.failed("project admin must not be permitted to update user's email")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')
