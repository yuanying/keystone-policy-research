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


class TestUserList(base.TestCase):

    def setUp(self):
        super(TestUserList, self).setUp()
        self.setup_project('project1', auditor=True)
        self.setup_project('project2', admin=False, user=0)

    def tearDown(self):
        super(TestUserList, self).tearDown()
        self.teardown_project('project1', auditor=True)
        self.teardown_project('project2', admin=False, user=0)

    def _list_all_or_project_user(self, target_project=None, username=None, project_name=None):
        command = ['user', 'list']
        if target_project is not None:
            command = command + ['--project', target_project.id]
        return self.os_run(
            command=command,
            project=project_name,
            username=username,
        )

    def assertListAllUser(self, username, project_name):
        self.assertGreaterEqual(
            len(self._list_all_or_project_user(username=username, project_name=project_name)),
            3
        )

    def assertNotListAllUser(self, username, project_name):
        try:
            self._list_all_or_project_user(username=username, project_name=project_name)
            self.fail("{} must not be permitted to list all user".format(username))
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    def assertListProjectUser(self, target_project, username, project_name):
        expected_users = self.admin.role_assignments.list(project=target_project.id)
        self.assertEqual(
            len(expected_users),
            len(self._list_all_or_project_user(target_project=target_project, username=username, project_name=project_name))
        )

    def assertNotListProjectUser(self, target_project, username, project_name):
        try:
            self._list_all_or_project_user(target_project=target_project, username=username, project_name=project_name)
            self.fail("{} must not be permitted to list {} user".format(username, target_project.name))
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # クラウド管理者は全てのユーザリストを表示することができる。
    def test_list_all_users_by_cloud_admin(self):
        username = clients.OS_ADMIN_USERNAME
        project = clients.OS_ADMIN_PROJECT_NAME
        self.assertListAllUser(username, project)

    # クラウド監査役は全てのユーザリストを表示することができる。
    def test_list_all_users_by_cloud_admin_auditor(self):
        username = self.admin_auditor.name
        project = clients.OS_ADMIN_PROJECT_NAME
        self.assertListAllUser(username, project)

    # プロジェクト1管理者は全てのユーザリストを表示することができない。
    def test_list_all_users_by_project_admin(self):
        username = self.project1_admin.name
        project = self.project1.name
        self.assertNotListAllUser(username, project)

    # プロジェクト1監査役は全てのユーザリストを表示することができない。
    def test_list_all_users_by_project_auditor(self):
        username = self.project1_auditor.name
        project = self.project1.name
        self.assertNotListAllUser(username, project)

    # プロジェクト1ユーザは全てのユーザリストを表示することができない。
    def test_list_all_users_by_user(self):
        username = self.project1_user0.name
        project = self.project1.name
        self.assertNotListAllUser(username, project)

    # プロジェクト1管理者はプロジェクト1のユーザリストを表示することができる。
    def test_list_project_users_by_project_admin(self):
        username = self.project1_admin.name
        project = self.project1.name
        self.assertListProjectUser(self.project1, username, project)

    # プロジェクト1監査役はプロジェクト1のユーザリストを表示することができる。
    def test_list_project_users_by_project_admin(self):
        username = self.project1_auditor.name
        project = self.project1.name
        self.assertListProjectUser(self.project1, username, project)

    # プロジェクト1ユーザはプロジェクト1のユーザリストを表示することができない。
    def test_list_project_users_by_user(self):
        username = self.project1_user0.name
        project = self.project1.name
        self.assertNotListProjectUser(self.project1, username, project)

    # プロジェクト1管理者はプロジェクト2のメンバーとして、
    # プロジェクト1/2のユーザリストを表示することができない。
    def test_list_different_project_user_by_project_admin_user(self):
        with self.grant_role_temporary(self.project_member_role, self.project1_admin, self.project2):
            username = self.project1_admin.name
            project = self.project2.name
            # project2 で認証チェック。
            self.assertEqual(
                self.project1_admin.id,
                self.os_run(
                    project=project,
                    username=username,
                    command=['user', 'show', self.project1_admin.id],
                )['id']
            )
            self.assertNotListProjectUser(self.project1, username, project)
            self.assertNotListProjectUser(self.project2, username, project)

    # プロジェクト1監査役はプロジェクト2のメンバーとして、
    # プロジェクト1/2のユーザリストを表示することができない。
    def test_list_different_project_user_by_project_auditor_user(self):
        with self.grant_role_temporary(self.project_member_role, self.project1_auditor, self.project2):
            username = self.project1_auditor.name
            project = self.project2.name
            # project2 で認証チェック。
            self.assertEqual(
                self.project1_auditor.id,
                self.os_run(
                    project=project,
                    username=username,
                    command=['user', 'show', self.project1_admin.id],
                )['id']
            )
            self.assertNotListProjectUser(self.project1, username, project)
            self.assertNotListProjectUser(self.project2, username, project)
