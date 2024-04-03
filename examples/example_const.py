#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ********************************************************************************
# © 2024 Yunlin Tan. All Rights Reserved.
# ********************************************************************************

"""
@package examples.example_const.py

@brief python-teamcity example const, this file contains the constants used in the example.

@author Yunlin Tan

@date 3/16/2024

**Related Page**: https://github.com/norbread2003/python-teamcity

Arguments
---------
    - None

Update Record
-------------
    None

Depends On
----------
**Python Dependencies:**
    - None

**Other Dependencies:**
    - None
"""
import os

# It is recommended to obtain TeamCity authorization via environment variables.
TEAMCITY_SERVER = os.environ.get('TEAMCITY_SERVER', None)
TEAMCITY_TOKENS = os.environ.get('TEAMCITY_TOKENS', None)

EX_BUILD_ID = 35193036  # Replace with your build_id
EX_BUILD_TYPE_ID = 'Tools_TeamcityBuildStatsCollector_StaticDataCollection'  # Replace with your build_type_id
