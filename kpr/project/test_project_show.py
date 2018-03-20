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


class TestProjectShow(base.TestCase):

    def setUp(self):
        super(TestProjectShow, self).setUp()
        self.setup_project('project1', auditor=True, user=1)
        self.setup_project('project2', admin=False, user=0)

    def tearDown(self):
        super(TestProjectShow, self).tearDown()
        self.teardown_project('project1', auditor=True, user=1)
        self.teardown_project('project2', admin=False, user=0)

    def _show_project_id(self, project, run_user, run_user_project):
        return self.os_run(
            command=['project', 'show', project.id],
            project=run_user_project,
            username=run_user,
        )['id']

    def assertShowProject(self, project, run_user, run_user_project):
        self.assertEqual(
            project.id,
            self._show_project_id(project, run_user, run_user_project)
        )

    def assertNotShowProject(self, project, run_user, run_user_project):
        try:
            self._show_project_id(project, run_user, run_user_project)
            self.self.fail('{} must not be able to show {}'.format(run_user, project.name))
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # クラウド管理者は全てのプロジェクトを表示することができる。
    def test_get_all_projects_by_cloud_admin(self):
        run_user = clients.OS_ADMIN_USERNAME
        run_user_project = clients.OS_ADMIN_PROJECT_NAME
        self.assertShowProject(self.project1, run_user, run_user_project)
        self.assertShowProject(self.project2, run_user, run_user_project)

    # クラウド監査役は全てのプロジェクトを表示することができる。
    def test_get_all_projects_by_cloud_admin_auditor(self):
        run_user = self.admin_auditor.name
        run_user_project = clients.OS_ADMIN_PROJECT_NAME
        self.assertShowProject(self.project1, run_user, run_user_project)
        self.assertShowProject(self.project2, run_user, run_user_project)

    # project1 のプロジェクト管理者は project1 を表示することができる。
    def test_get_project1_by_project1_admin(self):
        run_user = self.project1_admin.name
        run_user_project = self.project1.name
        self.assertShowProject(self.project1, run_user, run_user_project)

    # project1 のプロジェクト管理者は project2 を表示することができない。
    def test_get_project2_by_project1_admin(self):
        run_user = self.project1_admin.name
        run_user_project = self.project1.name
        self.assertNotShowProject(self.project2, run_user, run_user_project)

    # project1 のプロジェクト監査役は project1 を表示することができる。
    def test_get_project1_by_project1_auditor(self):
        run_user = self.project1_auditor.name
        run_user_project = self.project1.name
        self.assertShowProject(self.project1, run_user, run_user_project)

    # project1 のプロジェクト監査役は project2 を表示することができない。
    def test_get_project2_by_project1_auditor(self):
        run_user = self.project1_auditor.name
        run_user_project = self.project1.name
        self.assertNotShowProject(self.project2, run_user, run_user_project)

    # project1 のプロジェクトユーザは project1 を表示することができる。
    def test_get_project1_by_project1_user(self):
        run_user = self.project1_user0.name
        run_user_project = self.project1.name
        self.assertShowProject(self.project1, run_user, run_user_project)

    # project1 のプロジェクトユーザは project2 を表示することができない。
    def test_get_project2_by_project1_user(self):
        run_user = self.project1_user0.name
        run_user_project = self.project1.name
        self.assertNotShowProject(self.project2, run_user, run_user_project)
