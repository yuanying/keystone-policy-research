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
        self.setup_project('project1')
        self.setup_project('project2')

    def tearDown(self):
        super(TestUserList, self).tearDown()
        self.teardown_project('project1')
        self.teardown_project('project2')

    # クラウド管理者は全てのユーザリストを表示することができる。
    def test_list_all_users_by_cloud_admin(self):
        try:
            self.os_run(
                command=['user', 'list'],
                project=clients.OS_ADMIN_PROJECT_NAME,
                username=clients.OS_ADMIN_USERNAME,
            )
        except subprocess.CalledProcessError as e:
            self.failed("Failed to list all User by cloud admin")

    # プロジェクト1管理者は全てのユーザリストを表示することができない。
        try:
            self.os_run(
                project=self.project1.name,
                username=self.project1_admin.name,
                command=['user', 'list'],
            )
            self.failed("project admin must not be permitted to list all user")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # プロジェクト1ユーザは全てのユーザリストを表示することができない。
        try:
            self.os_run(
                project=self.project1.name,
                username=self.project1_user0.name,
                command=['user', 'list'],
            )
            self.failed("project admin must not be permitted to list all user")
        except subprocess.CalledProcessError as e:
            self.assertRegex(e.output.decode('utf-8'), 'HTTP 403')

    # プロジェクト1管理者はプロジェクト1のユーザリストを表示することができる。
    # プロジェクト1ユーザはプロジェクト1のユーザリストを表示することができない。

    # プロジェクト1管理者はプロジェクト2のメンバーとして、
    # プロジェクト2のユーザリストを表示することができない。