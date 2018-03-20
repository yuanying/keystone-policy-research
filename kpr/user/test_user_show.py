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
from keystoneauth1.exceptions import http
import subprocess

from kpr import base
from kpr.utils import clients


class TestUserShow(base.TestCase):

    def setUp(self):
        super(TestUserShow, self).setUp()
        self.setup_project('project1', user=1)
        self.setup_project('project2', user=1)

    def tearDown(self):
        super(TestUserShow, self).tearDown()
        self.teardown_project('project1', user=1)
        self.teardown_project('project2', user=1)

    def _show_user_id(self, target_user, user, project):
        return self.os_run(
            command=['user', 'show', target_user.id],
            username=user,
            project=project,
        )['id']

    @contextlib.contextmanager
    def grant_role_temporary(self, target_role, user, project):
        try:
            self.admin.roles.grant(
                target_role,
                user=user,
                project=project
            )
            yield
        except Exception as e:
            pass
        finally:
            self.admin.roles.revoke(
                target_role,
                user=user,
                project=project
            )

    def assertShowUser(self, target_user, user, project):
        self.assertEqual(
            target_user.id,
            self._show_user_id(target_user, user, project)
        )

    def assertNotShowUser(self, target_user, user, project):
        try:
            self._show_user_id(target_user, user, project)
            self.self.fail('{} must not be able to show {}'.format(user, target_user.name))
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')


    # クラウド管理者は全てのユーザを表示することができる。
    def test_get_all_users_by_cloud_admin(self):
        user = clients.OS_ADMIN_USERNAME
        project = clients.OS_ADMIN_PROJECT_NAME
        self.assertShowUser(self.project1_admin, user, project)
        self.assertShowUser(self.project2_admin, user, project)
        self.assertShowUser(self.project1_user0, user, project)
        self.assertShowUser(self.project2_user0, user, project)

    # クラウド監査役は全てのユーザを表示することができる。
    # TODO(yuanying): Let's test!

    # プロジェクト1管理者は自分を表示することができる。
    def test_get_self_by_project_admin(self):
        user = self.project1_admin.name
        project = self.project1.name
        self.assertShowUser(self.project1_admin, user, project)

    # プロジェクト1管理者はプロジェクト1のユーザを表示することができる。
    def test_get_same_project_user_by_project_admin(self):
        user = self.project1_admin.name
        project = self.project1.name
        self.assertShowUser(self.project1_user0, user, project)

    # プロジェクト1管理者はプロジェクト2のプロジェクト管理者を表示できない。
    def test_get_different_project_admin_by_project_admin(self):
        user = self.project1_admin.name
        project = self.project1.name
        self.assertNotShowUser(self.project2_admin, user, project)

    # プロジェクト1管理者はプロジェクト2のユーザを表示できない。
    def test_get_different_project_user_by_project_admin(self):
        user = self.project1_admin.name
        project = self.project1.name
        self.assertNotShowUser(self.project2_user0, user, project)

    # プロジェクト2のユーザ権限で認証されたプロジェクト1管理者はプロジェクト1のユーザを表示できない。
    def test_get_different_project_user_by_project_admin_user(self):
        with self.grant_role_temporary(self.project_member_role, self.project1_admin, self.project2):
            user = self.project1_admin.name
            project = self.project2.name
            # project2 で認証していても、自分を表示することは可能。
            self.assertShowUser(self.project1_admin, user, project)
            self.assertNotShowUser(self.project1_user0, user, project)

    # プロジェクト1監査役は自分を表示することができる。
    # TODO(yuanying): Let's test!

    # プロジェクト1監査役はプロジェクト1のユーザを表示することができる。
    # TODO(yuanying): Let's test!

    # プロジェクト1監査役はプロジェクト2のプロジェクト管理者を表示できない。
    # TODO(yuanying): Let's test!

    # プロジェクト1監査役はプロジェクト2のユーザを表示できない。
    # TODO(yuanying): Let's test!

    # プロジェクト2のユーザ権限で認証されたプロジェクト1監査役はプロジェクト1のユーザを表示できない。
    # TODO(yuanying): Let's test!
