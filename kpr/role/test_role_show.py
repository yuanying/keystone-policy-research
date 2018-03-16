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
        self.setup_project('project1', user=1)

    def tearDown(self):
        super(TestRoleShow, self).tearDown()
        self.teardown_project('project1', user=1)

    # クラウド管理者は全てのロールを表示することができる。
    # TODO(yuanying): Let's test!
    # クラウド監査役は全てのロールを表示することができる。
    # TODO(yuanying): Let's test!
    # project1 のプロジェクト管理者はロールを表示することができる。
    # TODO(yuanying): Let's test!
    # project1 のプロジェクト監査役はロールを表示することができる。
    # TODO(yuanying): Let's test!
    # project1 のプロジェクトユーザはロールを表示することができない。
    # TODO(yuanying): Let's test!
