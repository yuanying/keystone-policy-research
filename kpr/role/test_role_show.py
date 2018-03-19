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


class TestRoleShow(base.TestCase):

    def setUp(self):
        super(TestRoleShow, self).setUp()
        self.setup_project('project1', auditor=True, user=1)

    def tearDown(self):
        super(TestRoleShow, self).tearDown()
        self.teardown_project('project1', auditor=True, user=1)

    def all_roles(self):
        return [
            self.cloud_admin_role,
            self.cloud_admin_auditor_role,
            self.project_admin_role,
            self.project_auditor_role,
            self.project_member_role,
        ]

    def _test_get_all_roles(self, username, project_name):
        for role in self.all_roles():
            self.assertEqual(
                role.id,
                self.os_run(
                    command=['role', 'show', role.id],
                    project=project_name,
                    username=username,
                )['id']
            )

    # クラウド管理者はロールを表示することができる。
    # TODO(yuanying): Let's test!

    # クラウド監査役はロールを表示することができる。
    def test_get_all_roles_by_cloud_admin_auditor(self):
        self._test_get_all_roles(
            self.admin_auditor.name,
            clients.OS_ADMIN_PROJECT_NAME,
        )

    # project1 のプロジェクト管理者はロールを表示することができる。
    def test_get_all_roles_by_project1_admin(self):
        self._test_get_all_roles(
            self.project1_admin.name,
            self.project1.name,
        )

    # project1 のプロジェクト監査役はロールを表示することができる。
    def test_get_all_roles_by_project1_auditor(self):
        self._test_get_all_roles(
            self.project1_auditor.name,
            self.project1.name,
        )

    # project1 のプロジェクトユーザはロールを表示することができない。
    def test_get_all_roles_by_project1_member(self):
        username = self.project1_user0.name
        project_name = self.project1.name
        for role in self.all_roles():
            try:
                self.os_run(
                    command=['role', 'show', role.id],
                    project=project_name,
                    username=username,
                )
                self.fail("User '{}' must not show {}".format(
                    username, role.name
                ))
            except Exception as e:
                self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')
