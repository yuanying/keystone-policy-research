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

openstack role create project_admin

openstack project create project1 \
  --domain default \
  --enable
openstack project create project2 \
  --domain default \
  --enable

openstack user create project1_admin \
  --domain default \
  --project project1 \
  --password password

openstack role add \
  --user project1_admin \
  --project project1 \
  project_admin

openstack user create project1_user \
  --domain default \
  --project project1 \
  --password password

openstack user create project2_admin \
  --domain default \
  --project project2 \
  --password password

openstack role add \
  --user project2_admin \
  --project project2 \
  project_admin

openstack user create project2_user \
  --domain default \
  --project project2 \
  --password password

## Assign project1_admin to project2

openstack role add \
  --user project1_admin \
  --project project2 \
  Member
