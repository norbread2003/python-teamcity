#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ********************************************************************************
# © 2022-2024 Yunlin Tan. All Rights Reserved.
# ********************************************************************************

"""
@package examples.example_test.py

@brief python-teamcity example.

@author Yunlin Tan

@date 2/8/2024

**Related Page**: https://github.com/norbread2003/python-teamcity

Arguments
---------
    - None

Example Usage
-------------
    python3 examples/example_test.py

Update Record
-------------
    None

Depends On
----------
**Python Dependencies:**
    - python-teamcity

**Other Dependencies:**
    - None
"""
from examples.example_const import *
from teamcity import TeamCity

# Initialize the TeamCity object with your server and tokens
tc = TeamCity(server=TEAMCITY_SERVER, tokens=TEAMCITY_TOKENS)  # Recommended method

# Get latest successful build details of a specific build_type_id
latest_successful_build = tc.get_latest_build(build_type_id=EX_BUILD_TYPE_ID)
print(latest_successful_build)

# Get latest build details of a specific build_type_id
latest_build = tc.get_latest_build(build_type_id=EX_BUILD_TYPE_ID, success_only=False)
print(latest_build)

# Get details of a specific build using its build_id
build_details = tc.get_build_details(build_id=EX_BUILD_ID)  # Replace with your build_id
print(build_details)

# Get actual build parameters of the matching build.
build_parameters = tc.get_build_actual_parameters(build_id=EX_BUILD_ID)  # Replace with your build_id
print(build_parameters)

# Get specific actual build parameter of the matching build.
specific_parameters = tc.get_build_actual_parameters(build_id=EX_BUILD_ID, property_name='build.number')
print(specific_parameters)

# Get canceled info of a specific build by build_id
canceled_info = tc.get_canceled_info(build_id=EX_BUILD_ID)
print(canceled_info)

# # Get a list of all running builds
# running_builds = tc.get_running_builds()
# print(running_builds)
#
# # Get a list of artifacts for a specific build
# artifacts_list = tc.get_artifacts_list(build_id=20240001)
# print(artifacts_list)
#
# # Get the content of a specific artifact from a build
# artifact_content = tc.get_artifacts_content(build_id=20240001, artifact_path='path/to/artifact')
# print(artifact_content)
#
# # Get a list of build dependencies for a specific build
# build_dependencies = tc.get_build_dependencies(build_id=20240001)
# print(build_dependencies)
#
# # Get details of a specific user using their username
# user_details = tc.get_user(username='username')
# print(user_details)
#
# # Get a list of all users
# all_users = tc.get_all_users()
# print(all_users)
#
# # Cancel a specific build using its build_id
# tc.cancel_build(build_id=20240001)
#
# # Start a new build with a specific build_type_id
# tc.start_build(build_type_id='build_type_id')
#
# # Rerun a specific build using its build_id
# tc.rerun_build(build_id=20240001)
#
# # Get a list of all agents
# all_agents = tc.get_all_agents()
# print(all_agents)
#
# # Get details of a specific agent using their agent_id
# agent_details = tc.get_agent_details(agent_id=20240001)
# print(agent_details)
