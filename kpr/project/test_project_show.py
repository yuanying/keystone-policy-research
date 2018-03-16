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
        self.setup_project('project1', user=1)
        self.setup_project('project2', admin=False, user=0)

    def tearDown(self):
        super(TestProjectShow, self).tearDown()
        self.teardown_project('project1', user=1)
        self.teardown_project('project2', admin=False, user=0)

    # クラウド管理者は全てのプロジェクトを表示することができる。
    # TODO(yuanying): Let's test!
    # クラウド監査役は全てのプロジェクトを表示することができる。
    # TODO(yuanying): Let's test!
    # project1 のプロジェクト管理者は project1 を表示することができる。
    # TODO(yuanying): Let's test!
    # project1 のプロジェクト管理者は project2 を表示することができない。
    # TODO(yuanying): Let's test!
    # project1 のプロジェクト監査役は project1 を表示することができる。
    # TODO(yuanying): Let's test!
    # project1 のプロジェクト監査役は project2 を表示することができない。
    # TODO(yuanying): Let's test!
    # project1 のプロジェクトユーザは project1 を表示することができる。
    # TODO(yuanying): Let's test!
    # project1 のプロジェクトユーザは project2 を表示することができない。
    # TODO(yuanying): Let's test!
