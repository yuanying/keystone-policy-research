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

    def test_get_all_users_by_cloud_admin(self):
        self.assertEqual(
            self.project1_admin,
            self.admin.users.get(self.project1_admin)
        )
        self.assertEqual(
            self.project2_admin,
            self.admin.users.get(self.project2_admin)
        )
        self.assertEqual(
            self.project1_user,
            self.admin.users.get(self.project1_user)
        )
        self.assertEqual(
            self.project2_user,
            self.admin.users.get(self.project2_user)
        )
