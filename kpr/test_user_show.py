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

from keystoneauth1.exceptions import http
import subprocess

from kpr import base
from kpr.utils import clients


class TestUserShow(base.TestCase):

    def setUp(self):
        super(TestUserShow, self).setUp()
        self.setup_project('project1')
        self.setup_project('project2')

    def tearDown(self):
        super(TestUserShow, self).tearDown()
        self.teardown_project('project1')
        self.teardown_project('project2')

    # クラウド管理者は全てのユーザを表示することができる。
    def test_get_all_users_by_cloud_admin(self):
        self.assertEqual(
            self.project1_admin.id,
            self.os_run(
                command=['user', 'show', self.project1_admin.id],
                project=clients.OS_ADMIN_PROJECT_NAME,
                username=clients.OS_ADMIN_USERNAME,
            )['id']
        )
        self.assertEqual(
            self.project2_admin.id,
            self.os_run(
                command=['user', 'show', self.project2_admin.id],
                project=clients.OS_ADMIN_PROJECT_NAME,
                username=clients.OS_ADMIN_USERNAME,
            )['id']
        )
        self.assertEqual(
            self.project1_user0.id,
            self.os_run(
                command=['user', 'show', self.project1_user0.id],
                project=clients.OS_ADMIN_PROJECT_NAME,
                username=clients.OS_ADMIN_USERNAME,
            )['id']
        )
        self.assertEqual(
            self.project2_user0.id,
            self.os_run(
                command=['user', 'show', self.project2_user0.id],
                project=clients.OS_ADMIN_PROJECT_NAME,
                username=clients.OS_ADMIN_USERNAME,
            )['id']
        )

    # プロジェクト1管理者は自分を表示することができる。
    def test_get_self_by_project_admin(self):
        self.assertEqual(
            self.project1_admin.id,
            self.os_run(
                project=self.project1.name,
                username=self.project1_admin.name,
                command=['user', 'show', self.project1_admin.id],
            )['id']
        )

    # プロジェクト1管理者はプロジェクト1のユーザを表示することができる。
    def test_get_same_project_user_by_project_admin(self):
        self.assertEqual(
            self.project1_user0.id,
            self.os_run(
                project=self.project1.name,
                username=self.project1_admin.name,
                command=['user', 'show', self.project1_user0.id],
            )['id']
        )

    # プロジェクト1管理者はプロジェクト2のプロジェクト管理者を表示できない。
    def test_get_different_project_admin_by_project_admin(self):
        try:
            self.os_run(
                project=self.project1.name,
                username=self.project1_admin.name,
                command=['user', 'show', self.project2_admin.id],
            )
            self.fail("User '{}' must not show {}".format(
                'project1_admin', 'project2_admin'
            ))
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # プロジェクト1管理者はプロジェクト2のユーザを表示できない。
    def test_get_different_project_user_by_project_admin(self):
        try:
            self.os_run(
                project=self.project1.name,
                username=self.project1_admin.name,
                command=['user', 'show', self.project2_user0.id],
            )
            self.fail("User '{}' must not show {}".format(
                'project1_admin', 'project2_user0'
            ))
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # プロジェクト2のユーザ権限で認証されたプロジェクト1管理者はプロジェクト1のユーザを表示できない。
    def test_get_different_project_user_by_project_admin_user(self):
        try:
            self.admin.roles.grant(
                self.project_member_role,
                user=self.project1_admin,
                project=self.project2
            )
            # project2 で認証していても、自分を表示することは可能。
            self.assertEqual(
                self.project1_admin.id,
                self.os_run(
                    project=self.project2.name,
                    username=self.project1_admin.name,
                    command=['user', 'show', self.project1_admin.id],
                )['id']
            )
            try:
                self.os_run(
                    project=self.project2.name,
                    username=self.project1_admin.name,
                    command=['user', 'show', self.project1_user0.id],
                )
                self.fail("User '{}' must not show {}".format(
                    'project1_admin', 'project1_user0'
                ))
            except subprocess.CalledProcessError as e:
                self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')
        except Exception as e:
            pass
        finally:
            self.admin.roles.revoke(
                self.project_member_role,
                user=self.project1_admin,
                project=self.project2
            )
