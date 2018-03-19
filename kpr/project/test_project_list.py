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


class TestProjectList(base.TestCase):

    def setUp(self):
        super(TestProjectList, self).setUp()
        self.setup_project('project1', auditor=True, user=1)
        self.setup_project('project2', admin=False, user=0)

    def tearDown(self):
        super(TestProjectList, self).tearDown()
        self.teardown_project('project1', auditor=True, user=1)
        self.teardown_project('project2', admin=False, user=0)

    def _list_all_projects(self, username, project_name):
        return self.os_run(
            command=['project', 'list'],
            project=project_name,
            username=username,
        )

    def _list_all_projects_with_success(self, username, project_name):
        self.assertGreaterEqual(
            len(self._list_all_projects(username, project_name)),
            3
        )

    def _list_all_projects_with_fail(self, username, project_name):
        self.assertLess(
            len(self._list_all_projects(username, project_name)),
            3
        )

    # クラウド管理者は全てのプロジェクトを一覧表示することができる。
    def test_list_all_projects_by_cloud_admin(self):
        self._list_all_projects_with_success(
            clients.OS_ADMIN_USERNAME,
            clients.OS_ADMIN_PROJECT_NAME
        )

    # クラウド監査役は全てのプロジェクトを一覧表示することができる。
    def test_list_all_projects_by_cloud_admin_auditor(self):
        self._list_all_projects_with_success(
            self.admin_auditor.name,
            clients.OS_ADMIN_PROJECT_NAME
        )

    # project1 のプロジェクト管理者はプロジェクトを一覧表示することができない。
    def test_list_all_projects_by_project_admin(self):
        self._list_all_projects_with_fail(
            self.project1_admin.name,
            self.project1.name
        )

    # project1 のプロジェクト監査役はプロジェクトを一覧表示することができない。
    def test_list_all_projects_by_project_auditor(self):
        self._list_all_projects_with_fail(
            self.project1_auditor.name,
            self.project1.name
        )

    # project1 のプロジェクトユーザはプロジェクトを一覧表示することができない。
    def test_list_all_projects_by_project_user(self):
        self._list_all_projects_with_fail(
            self.project1_user0.name,
            self.project1.name
        )
