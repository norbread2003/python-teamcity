#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ********************************************************************************
# © 2022-2024 Yunlin Tan. All Rights Reserved.
# ********************************************************************************

"""
@package teamcity.teamcity

@brief Python API for triggering TeamCity by REST API.

@author Yunlin Tan

@date 11/22/2022

**Related Page**: https://github.com/norbread2003/python-teamcity
**Reference Page**: https://www.jetbrains.com/help/teamcity/rest/teamcity-rest-api-documentation.html

Arguments
---------
    - None

Example Usage
-------------
    python3 examples/example_test.py

Update Record
-------------
0.1.0.1122   11/22/2022   Yunlin Tan([None])            Python API for triggering TeamCity by REST API.
0.1.1        11/25/2022   Yunlin Tan([None])            Add more functions by requests.
0.1.5        5/25/2023    Yunlin Tan([None])            Multiple features added.
0.1.6        5/26/2023    Yunlin Tan([None])            Optimize get_build_dependencies function.
0.1.7        8/29/2023    Yunlin Tan([None])            Support to get build artifacts content.
0.1.8        10/15/2023   Yunlin Tan([None])            Support starting and canceling builds.
0.1.9        10/18/2023   Yunlin Tan([None])            Support rerunning builds.
0.2.0        11/13/2023   Yunlin Tan([None])            Change packing method.
0.2.1        1/23/2024    Yunlin Tan([None])            Add agent-related functions.
0.2.1        1/23/2024    Yunlin Tan([None])            Support to get agent details.
0.2.3        2/1/2024     Yunlin Tan([None])            Support to get all agents (including unauthorized).
0.2.4        3/4/2024     Yunlin Tan([None])            Support to get actual build parameters by resulting-properties.
0.2.5        3/13/2024    Yunlin Tan([None])            Add more functions to get builds.
0.2.9        4/3/2024     Yunlin Tan([None])            Support to get latest build detail by build type id.
0.3.0        4/8/2024     Yunlin Tan([None])            Support to get build queue changes.

Depends On
----------
**Python Dependencies:**
    - requests

**Other Dependencies:**
    - None
"""
import logging
import os

import requests

from teamcity.teamcity_const import AuthMethod, RequestMethod, RequestReturnType


class TeamCity:
    def __init__(self, server=None, tokens=None, user=None, password=None, guest=False):
        self.server = self.process_server_address(server or os.environ.get('TEAMCITY_SERVER', None))
        self.tokens = tokens or os.environ.get('TEAMCITY_TOKENS', None)
        self.user = user or os.environ.get('TEAMCITY_USER', None)
        self.password = password or os.environ.get('TEAMCITY_PASSWORD', None)
        self.guest = guest or os.environ.get('TEAMCITY_GUEST', False)
        self.authentication_method, self.base_url, self.header = self.check_auth_method()

    @staticmethod
    def process_server_address(server: object):
        """Process server address."""
        if not server:
            logging.error('Failed to detect TeamCity server.')
            raise ValueError('TeamCity server is not set.')

        server = server[:-1] if server.endswith('/') else server
        return server if server.startswith('http://') or server.startswith('https://') else f'https://{server}'

    def check_auth_method(self):
        """Check authentication method and return related info."""

        header = {'Accept': 'application/json'}
        if self.tokens:
            logging.info(f'Logging in TeamCity with tokens.')
            authentication_method = AuthMethod.TOKENS
            base_url = f'{self.server}/app/rest'
            header.update({'Authorization': f'Bearer {self.tokens}'})
        elif self.user and self.password:
            logging.info(f'Logging TeamCity with user: {self.user}')
            authentication_method = AuthMethod.USER
            base_url = f'{self.server}/httpAuth/app/rest'
        elif self.guest:  # Guest login
            logging.info(f'Logging TeamCity as guest.')
            authentication_method = AuthMethod.GUEST
            base_url = f'{self.server}/guestAuth/app/rest'
        else:  # No authentication
            logging.warning('No authentication method provided, assume you are logged in to TeamCity in the browser.')
            logging.warning('If you are not logged in, you will get 401 Unauthorized error.')
            authentication_method = AuthMethod.LOGGED_IN
            base_url = f'{self.server}/app/rest'
        return authentication_method, base_url, header

    def request_base(self, url, method, extra_headers=None, data=None, json=None, timeout=None, retries=3):
        url, headers = f'{self.base_url}/{url}', self.header
        extra_headers = {} if extra_headers is None else extra_headers
        headers.update(extra_headers)
        session = requests.Session()
        logging.info(f'Calling TeamCity API: {url}')

        response = None
        while retries > 0:
            try:
                if self.authentication_method in [AuthMethod.TOKENS, AuthMethod.GUEST]:
                    response = session.request(method, url, headers=headers, data=data, json=json, timeout=timeout)
                elif self.authentication_method == AuthMethod.USER:
                    response = session.request(method, url, auth=(self.user, self.password), headers=headers,
                                               data=data, json=json, timeout=timeout)
                elif self.authentication_method == AuthMethod.LOGGED_IN:
                    logging.error('You are not logged in to TeamCity, POST method is not supported.')
                    raise ValueError('You are not logged in to TeamCity, POST method is not supported.')
                else:
                    logging.error('Unknown authentication method.')
                    raise ValueError('Unknown authentication method.')

            except Exception as e:
                logging.error(f'Failed to {method.lower()} request to TeamCity: {e}, retries left: {retries}')

            if response is None or response.status_code != 200:
                return_code = response.status_code if response is not None else 'NA'
                logging.error(f'Failed to {method.lower()} request to TeamCity: {return_code}, retries left: {retries}')
            else:
                return response

            retries -= 1
        else:
            return_code = response.status_code if response is not None else 'NA'
            logging.error(f'No retries left, failed to {method.lower()} request to TeamCity: {return_code}')
            raise ValueError(f'No retries left, failed to {method.lower()} request to TeamCity: {return_code}')

    def post_request(self, url, extra_headers=None, data=None, json=None, timeout=None, retries=3):
        extra_headers = {} if extra_headers is None else extra_headers
        extra_headers.update({'Content-Type': 'application/json'})
        return self.request_base(url=url, method='POST', extra_headers=extra_headers, data=data, json=json,
                                 timeout=timeout, retries=retries)

    def get_request(self, url, extra_headers=None, data=None, json=None, timeout=None, retries=3):
        extra_headers = {} if extra_headers is None else extra_headers
        extra_headers.update({'Accept': 'application/json'})
        return self.request_base(url=url, method='GET', extra_headers=extra_headers, data=data, json=json,
                                 timeout=timeout, retries=retries).json()

    def get_string_request(self, url, extra_headers=None, data=None, json=None, timeout=None, retries=3):
        extra_headers = {} if extra_headers is None else extra_headers
        extra_headers.update({'Accept': 'text/plain'})
        return self.request_base(url=url, method='GET', extra_headers=extra_headers, data=data, json=json,
                                 timeout=timeout, retries=retries).text

    def get_file_request(self, url, extra_headers=None, data=None, json=None, timeout=None, retries=3):
        extra_headers = {} if extra_headers is None else extra_headers
        extra_headers.update({'Accept': 'application/json'})
        return self.request_base(url=url, method='GET', extra_headers=extra_headers, data=data, json=json,
                                 timeout=timeout, retries=retries).text

    def get_all_builds(self, build_type_id='', details=False, count=10000):
        """Get builds from TeamCity.

        Default count is 1e5. Extend it if necessary, but it will affect teamcity server performance.
        REST API Reference: https://www.jetbrains.com/help/teamcity/rest/get-build-details.html
        """
        url = f'builds?locator=defaultFilter:false,count:{count}'
        if build_type_id != '':
            url += f',buildType:(id:{build_type_id})'
        data = self.get_request(url)['build']
        return [self.get_build_details(build['id']) for build in data] if details else data

    def get_builds_by_date(self, start_date='', finish_date='', build_type_id='', details=False, count=100000):
        """Get builds by date from TeamCity."""
        url = f'builds?locator=defaultFilter:false,count:{count}'
        if build_type_id != '':
            url += f',buildType:(id:{build_type_id})'
        if start_date != '':
            url += f',startDate:{start_date}'
        if finish_date != '':
            url += f',finishDate:{finish_date}'
        data = self.get_request(url)['build']
        return [self.get_build_details(build['id']) for build in data] if details else data

    def get_builds_by_since_build(self, since_build_id='', build_type_id='', details=True, count=10000):
        """Get builds by since build from TeamCity."""
        if build_type_id != '' and not details:
            raise Exception('Currently only the default "build_type_id" and "details" parameters are supported.')

        default_builds = sorted(self.get_custom_builds(default=True), key=lambda x: x['id'], reverse=True)
        # TODO(yunlin): latest_build_id is the latest build id of the successful build, not the latest build id
        latest_build_id = default_builds[0]['id'] if len(default_builds) > 0 else 0

        result = []
        if since_build_id > latest_build_id:
            logging.info(f'No new builds since build {since_build_id}')
            return result

        logging.info(f'Start to get builds from build {since_build_id} to build {latest_build_id}')
        for build_id in range(since_build_id, latest_build_id + 1):
            single_build = self.get_build_details(build_id)
            if single_build != dict() and single_build['id'] == build_id:
                result.append(single_build)
            else:
                # TODO(yunlin): Need to fix build id extremely small issue.
                logging.info(f'Build {build_id} does not exist')
                logging.warning(f'Please confirm the existence of the build id you provided. '
                                f'Otherwise the function will keep polling and will not stop. '
                                f'This issue will be fixed in the future.')
            if len(result) >= count:
                break
        return result

    def get_custom_builds(self, locator='', build_type_id='', default=False, details=False, count=100000):
        """Get builds by custom locator from TeamCity."""
        if default:
            url = f'builds?locator=count:{100 if count == 100000 else count}'
        else:
            url = f'builds?locator=defaultFilter:false,count:{count}'
        if locator != '':
            url += f',{locator}'
        if build_type_id != '':
            url += f',buildType:(id:{build_type_id})'
        data = self.get_request(url)['build']
        return [self.get_build_details(build['id']) for build in data] if details else data

    def get_queued_builds(self, build_type_id='', details=False, count=5000):
        """Get queued builds from TeamCity."""
        url = f'buildQueue?locator=count:{count}'
        if build_type_id != '':
            url += f',buildType:(id:{build_type_id})'
        data = self.get_request(url)['build']
        return [self.get_build_details(build['id']) for build in data] if details else data

    def get_running_builds(self, build_type_id='', details=True, count=5000):
        """Get running builds from TeamCity."""
        url = f'builds?locator=defaultFilter:false,count:{count},running:true'
        if build_type_id != '':
            url += f',buildType:(id:{build_type_id})'
        data = self.get_request(url)['build']
        return [self.get_build_details(build['id']) for build in data] if details else data

    def get_latest_build(self, build_type_id='', success_only=True):
        """Get latest build from TeamCity.
        :param build_type_id: build type id in TeamCity, must be provided.
        :param success_only: True to get the latest successful build, False to get the latest build.
        :return: dict format latest build details, empty dict if no build found.

        """
        if success_only:
            url = f'builds?locator=defaultFilter:false,count:1,status:SUCCESS'
        else:
            url = f'builds?locator=defaultFilter:false,count:1'
        if build_type_id != '':
            url += f',buildType:(id:{build_type_id})'
        data = self.get_request(url)['build']
        return self.get_build_details(data[0]['id']) if data else dict()

    def get_build_details(self, build_id):
        """Get detail build by build id from TeamCity."""
        url = f'builds/id:{build_id}'
        try:
            return self.get_request(url)
        except Exception as ex:
            logging.error(ex)
            logging.error(f'Failed to get build {build_id} details.')
            return dict()

    def get_canceled_info(self, build_id):
        """Get canceled info by build id from TeamCity."""
        url = f'builds/id:{build_id}/canceledInfo'
        try:
            return self.get_request(url)
        except Exception as ex:
            logging.error(ex)
            logging.error(f'Failed to get build {build_id} canceled info.')
            return dict()

    # def build_api_base(self, url, method, return_type=None, build_id='', locator=''):
    #     return_type = RequestReturnType.NONE if method == RequestMethod.POST else return_type
    #     try:
    #         if type(method) is str and method.upper() not in [RequestMethod.GET, RequestMethod.POST]:
    #             raise ValueError(f'Invalid method {method}. Only GET, POST are supported.')
    #         if type(return_type) is str and method.lower() not in [RequestReturnType.JSON, RequestReturnType.TEXT,
    #                                                                RequestReturnType.FILE]:
    #             raise ValueError(f'Invalid return type {return_type}. Only JSON, TEXT, FILE are supported.')
    #         if url == '':
    #             raise ValueError('Please provide a valid url.')
    #         if build_id != '' and locator == '':
    #             raise ValueError('Please provide a valid build_id or locator.')
    #
    #         if build_id != '' and locator != '':  # TODO(yunlin): Need to fix this issue.
    #             url = url.replace('{{buildLocator}}', locator)
    #         elif build_id != '':
    #             url = url.replace('{{buildLocator}}', f'id:{build_id}')
    #         elif locator != '':
    #             url = url.replace('{{buildLocator}}', locator)
    #
    #         if method.upper() == RequestMethod.GET:
    #             if return_type == RequestReturnType.JSON:
    #                 return self.get_request(url)
    #             elif return_type == RequestReturnType.TEXT:
    #                 return self.get_string_request(url)
    #             elif return_type == RequestReturnType.FILE:
    #                 return self.get_file_request(url)
    #             else:
    #                 return None
    #         elif method.upper() == RequestMethod.POST:
    #             return self.post_request(url)
    #     except Exception as ex:
    #         logging.error(ex)
    #         if return_type == RequestReturnType.JSON:
    #             return dict()
    #         elif return_type == RequestReturnType.TEXT or return_type == RequestReturnType.FILE:
    #             return ''
    #         elif return_type == RequestReturnType.NONE:
    #             return False
    #         else:
    #             return None
    #
    # def get_aggregated_build_status(self, build_id='', locator=''):
    #     """Get the build status of aggregated matching builds.
    #
    #     :param build_id: TeamCity build id.
    #     :param locator: TeamCity build locator, should be provided if build id is not available.
    #                     If both parameters are provided, both will be used.
    #
    #     :return:
    #     """
    #     url = f'/app/rest/builds/aggregated/{{buildLocator}}/status'

    def get_build_actual_parameters(self, build_id, property_name=''):
        """Get actual build parameters of the matching build by resulting-properties from TeamCity.

        Reference Page: https://www.jetbrains.com/help/teamcity/rest/buildapi.html#getBuildActualParameters

        :param build_id: TeamCity build id.
        :param property_name: A valid property name could be empty.
        :return: List format actual parameters or string format specific result attributes.
        """
        try:
            if property_name == '':
                url = f'builds/id:{build_id}/resulting-properties'
                return self.get_request(url)['property']
            else:
                url = f'builds/id:{build_id}/resulting-properties/{property_name}'
                return self.get_string_request(url)
        except Exception as ex:
            logging.error(ex)
            logging.error(f'Failed to get build {build_id} actual parameters.')
            return list() if property_name == '' else None

    def get_build_resulting_properties(self, build_id, property_name):
        """Get the specific resulting properties of the matching build from TeamCity.

        Reference Page: https://www.jetbrains.com/help/teamcity/rest/buildapi.html#getBuildResultingProperties

        :param build_id: TeamCity build id.
        :param property_name: A valid property name must be provided.
        :return: String format specific result attributes.
        """
        if property_name == '':
            logging.error('Property name is empty. '
                          'Please provide a valid property name or use get_build_actual_parameters instead.')
            return None
        return self.get_build_actual_parameters(build_id, property_name)

    def get_artifacts_list(self, build_id):
        """Get artifacts list by build id from TeamCity."""
        url = f'builds/id:{build_id}/artifacts'
        try:
            return self.get_request(url)['file']
        except Exception as ex:
            logging.error(ex)
            logging.error(f'Failed to get build {build_id} artifacts.')
            return list()

    def get_artifacts_content(self, build_id, artifact_path):
        """Get artifacts content by build id and artifact path from TeamCity."""
        artifact_list = self.get_artifacts_list(build_id)
        for artifact in artifact_list:
            if artifact['name'] == artifact_path:
                url = f'builds/id:{build_id}/artifacts/content/{artifact_path}'
                try:
                    return self.get_file_request(url)
                except Exception as ex:
                    logging.error(ex)
                    logging.error(f'Failed to get build {build_id} artifact {artifact_path} content.')
                    return ''
        logging.error(f'Failed to get build {build_id} artifact {artifact_path} content.')
        return ''

    def get_build_dependencies(self, build_id, count=10000):
        """Get build dependencies by build id from TeamCity."""
        url = f'builds?locator=defaultFilter:false,' \
              f'snapshotDependency(to:(id:{build_id})),count:{count},or:(personal:false,and:(personal:true,' \
              f'user:current))&fields=count,build(id,number,branchName,defaultBranch,queuedDate,startDate,' \
              f'finishDate,history,composite,links(link(type,relativeUrl)),comment(text,timestamp,user(id,' \
              f'name,username)),statusChangeComment(text,timestamp,user(id,name,username)),statusText,' \
              f'status,state,failedToStart,personal,detachedFromAgent,finishOnAgentDate,pinned,pinInfo(' \
              f'text,timestamp,user(id,name,username)),user(id,name,username),customization,canceledInfo(' \
              f'text,user(id,name,username)),agent(name,id,links(link(type,relativeUrl)),environment(' \
              f'osType),typeId,connected,pool(id,name)),tags(tag(name,private),$locator(private:any,' \
              f'owner:current)),artifacts($locator(count:1),count:($optional)),limitedChangesCount(' \
              f'$optional),buildType(id,paused,internalId,projectId,name,type,links(link(type,' \
              f'relativeUrl))),snapshot-dependencies(count,build(id)),running-info(percentageComplete,' \
              f'elapsedSeconds,estimatedTotalSeconds,leftSeconds,probablyHanging,lastActivityTime,outdated,' \
              f'outdatedReasonBuild(number,links(link(type,relativeUrl)))),waitReason,queuePosition,' \
              f'startEstimate,finishEstimate,plannedAgent(name,id,environment(osType),typeId,pool(id,name)),' \
              f'delayedByBuild(id,number,status,state,failedToStart,personal,canceledInfo,buildType(id)),' \
              f'triggered(date,displayText,buildType(id,paused,internalId,projectId,name,type,links(' \
              f'link(type,relativeUrl)))))'
        data = self.get_request(url)['build']
        return data if data else []

    def get_all_changes(self, build_type_id='', locator='', count=10000):
        """Get all changes by build type id from TeamCity."""
        url = f'changes?count:{count}'
        if build_type_id != '':
            url += f',buildType:(id:{build_type_id})'
        if locator != '':
            url += f',{locator}'
        try:
            data = self.get_request(url)['change']
            return data
        except Exception as ex:
            logging.error(ex)
            logging.error(f'Failed to get all changes from TeamCity.')
            return list()

    def get_pending_changes(self, build_type_id='', locator=''):
        """Get pending changes by build type id from TeamCity."""
        url = f'changes?locator=buildType:(id:{build_type_id}),pending:true'
        if locator != '':
            url += f',{locator}'
        try:
            data = self.get_request(url)
            if len(data) > 0 and 'change' in data:
                return data['change']
            else:
                logging.info(f'No pending changes found for build type {build_type_id}.')
                return list()
        except Exception as ex:
            logging.error(ex)
            logging.error(f'Failed to get pending changes from TeamCity.')
            return list()

    def get_user(self, username='') -> dict:
        """Get user by username from TeamCity.

        :param username: username, if empty - get current user
        :return: user dict, for example:

        {'username': 'teamcity', 'name': 'Teamcity', 'id': 200, 'email': 'support@jetbrains.com',
         'lastLogin': '20230122T192035+0800', 'href': '/app/rest/users/id:200', }
        """
        url = f'users/id:{username}' if username else 'users/current'
        return self.get_request(url)

    def get_all_users(self) -> list:
        """Get all users from TeamCity.

        :return: list of users, for example:

        [{'username': 'teamcity', 'name': 'Teamcity', 'id': 200, 'email': '},]
        """
        url = 'users'
        return self.get_request(url)['user']

    def cancel_build(self, build_id):
        """Cancel build by build id from TeamCity."""
        queue_url = f'buildQueue?locator=id:{build_id}'
        if len(self.get_request(queue_url)['build']) > 0:
            return self.post_request(f'buildQueue/id:{build_id}',
                                     json={'comment': 'Cancelled by python-teamcity',
                                           'readdIntoQueue': False})
        else:
            if self.get_build_details(build_id).get('state', '') == 'running':
                return self.post_request(f'builds/id:{build_id}',
                                         json={'comment': 'Cancelled by python-teamcity',
                                               'readdIntoQueue': False})
            else:
                logging.error(f'Build {build_id} is not running or in queue.')
                return False

    def start_build(self, build_type_id, comment='', parameters=None, custom_data=None):
        """Start build by build type id from TeamCity."""
        url = f'buildQueue'
        tc_json = {"buildType": {"id": build_type_id},
                   "comment": {"text": comment}}
        if parameters:
            tc_json['properties'] = {"property": parameters}
        if custom_data:
            tc_json.update(custom_data)
        return self.post_request(url, json=tc_json)

    def rerun_build(self, build_id, parameters=True):
        """Rerun build by build id from TeamCity."""
        origin = self.get_build_details(build_id)
        if origin is None or origin.get('buildType', {}).get('id', '') == '':
            logging.error(f'Build {build_id} does not exist.')
            return False
        build_type_id, rerun_parameters = origin['buildType']['id'], []
        if parameters and origin.get('properties', {}).get('property', []) != []:
            for tc_property in origin['properties']['property']:
                if 'inherited' not in tc_property:
                    rerun_parameters.append({'name': tc_property['name'], 'value': tc_property['value']})
        rerun_parameters = None if not rerun_parameters else rerun_parameters
        return self.start_build(build_type_id, comment=f'Rerun build {build_id} by python-teamcity',
                                parameters=rerun_parameters)

    def get_all_agents(self, details=False, authorized='true'):
        """Get all agents from TeamCity."""
        url = f'agents?locator=authorized:{authorized}'
        try:
            data = self.get_request(url)['agent']
            return [self.get_agent_details(build['id']) for build in data] if details else data
        except Exception as ex:
            logging.error(ex)
            logging.error(f'Failed to get all agents from TeamCity.')
            return list()

    def get_agent_details(self, agent_id):
        """Get detail agent by agent id from TeamCity."""
        url = f'agents/id:{agent_id}'
        try:
            return self.get_request(url)
        except Exception as ex:
            logging.error(ex)
            logging.error(f'Failed to get agent {agent_id} details')
            return dict()
