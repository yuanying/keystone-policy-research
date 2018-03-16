#!/usr/bin/env bash

# openstack user create test3 \
#   --domain default \
#   --project demo \
#   --password password
#
# openstack role add \
#   --user test3 \
#   --project demo \
#   admin

##

openstack role create admin_auditor
openstack role create project_auditor
openstack role create project_admin

openstack project create projectA \
  --domain default \
  --enable
openstack project create projectB \
  --domain default \
  --enable

openstack user create projectA_admin \
  --domain default \
  --project projectA \
  --password password

openstack role add \
  --user projectA_admin \
  --project projectA \
  project_admin

openstack user create projectA_user \
  --domain default \
  --project projectA \
  --password password

openstack role add \
  --user projectA_user \
  --project projectA \
  Member

openstack user create projectB_admin \
  --domain default \
  --project projectB \
  --password password

openstack role add \
  --user projectB_admin \
  --project projectB \
  project_admin

openstack user create projectB_user \
  --domain default \
  --project projectB \
  --password password

openstack role add \
  --user projectB_user \
  --project projectB \
  Member

## Assign project1_admin to project2

openstack role add \
  --user projectA_admin \
  --project projectB \
  Member
