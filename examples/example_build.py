#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ********************************************************************************
# © 2024 Yunlin Tan. All Rights Reserved.
# ********************************************************************************

"""
@package examples.example_test.py

@brief python-teamcity example.

@author Yunlin Tan

@date 8/1/2024

**Related Page**: https://github.com/norbread2003/python-teamcity

Arguments
---------
    - None

Example Usage
-------------
    python3 examples/example_build.py

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

# Get the latest successful build details of a specific build_type_id
latest_successful_build = tc.get_latest_build(build_type_id=EX_BUILD_TYPE_ID)
print(latest_successful_build)

build_step_info = tc.get_build_steps(build_id=latest_successful_build['id'])