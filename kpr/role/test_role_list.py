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


class TestRoleList(base.TestCase):

    def setUp(self):
        super(TestRoleList, self).setUp()
        self.setup_project('project1', auditor=True, user=1)
        self.setup_project('project2', admin=False, auditor=False, user=0)

    def tearDown(self):
        super(TestRoleList, self).tearDown()
        self.teardown_project('project1', auditor=True, user=1)
        self.teardown_project('project2', admin=False, auditor=False, user=0)

    # クラウド管理者は全てのロールを一覧表示することができる。
    def test_list_all_roles_by_cloud_admin(self):
        try:
            self.os_run(
                command=['role', 'list'],
                project=clients.OS_ADMIN_PROJECT_NAME,
                username=clients.OS_ADMIN_USERNAME,
            )
        except subprocess.CalledProcessError as e:
            self.fail("Failed to list all Roles by cloud admin")

    # クラウド監査役は全てのロールを一覧表示することができる。
    def test_list_all_roles_by_cloud_admin_auditor(self):
        try:
            self.os_run(
                command=['role', 'list'],
                project=clients.OS_ADMIN_PROJECT_NAME,
                username=self.admin_auditor.name,
            )
        except subprocess.CalledProcessError as e:
            self.fail("Failed to list all Roles by cloud admin auditor")

    # project1 の管理者はロールを一覧表示することができる。
    def test_list_all_roles_by_project_admin(self):
        try:
            self.os_run(
                command=['role', 'list'],
                project=self.project1.name,
                username=self.project1_admin.name,
            )
        except subprocess.CalledProcessError as e:
            self.fail("Failed to list all Roles by project admin")

    # project1 の監査役はロールを一覧表示することができる。
    def test_list_all_roles_by_project_auditor(self):
        try:
            self.os_run(
                command=['role', 'list'],
                project=self.project1.name,
                username=self.project1_auditor.name,
            )
        except subprocess.CalledProcessError as e:
            self.fail("Failed to list all Roles by project auditor")

    # project1 のユーザはロールを一覧表示することができない。
    def test_list_all_roles_by_project_user(self):
        try:
            self.os_run(
                project=self.project1.name,
                username=self.project1_user0.name,
                command=['role', 'list'],
            )
            self.fail("project user must not be permitted to list all role")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')
