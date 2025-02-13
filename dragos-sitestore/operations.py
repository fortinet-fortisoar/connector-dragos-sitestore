"""
Copyright start
MIT License
Copyright (c) 2025 Fortinet Inc
Copyright end
"""

import base64
import requests, json
from .constant import *
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('dragos-sitestore')


class Dragos(object):
    def __init__(self, config, *args, **kwargs):
        self.api_id = config.get('api_id')
        self.api_secret = config.get('api_secret')
        url = config.get('server_url').strip('/')
        if not url.startswith('https://') and not url.startswith('http://'):
            self.url = 'https://{0}/'.format(url)
        else:
            self.url = url + '/'
        credentials = f"{self.api_id}:{self.api_secret}"
        self.base64_encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        self.verify_ssl = config.get('verify_ssl')

    def make_rest_call(self, endpoint, method, data=None, params=None):
        try:
            url = self.url + endpoint
            headers = {
                'Authorization': 'Basic {0}'.format(self.base64_encoded),
                'Content-Type': 'application/json'
            }
            logger.debug("Endpoint {0}".format(url))
            response = requests.request(method, url, data=data, params=params,
                                        headers=headers, verify=self.verify_ssl)
            logger.debug("response_content {0}:{1}".format(response.status_code, response.content))
            if response.ok or response.status_code == 204:
                logger.info('Successfully got response for url {0}'.format(url))
                if 'json' in str(response.headers):
                    return response.json()
                else:
                    return response
            else:
                logger.error("{0}".format(response.status_code))
                raise ConnectorError("{0}:{1}".format(response.status_code, response.text))
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError(
                'The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Invalid Credentials')
        except Exception as err:
            raise ConnectorError(str(err))


def check_payload(payload):
    updated_payload = {}
    for key, value in payload.items():
        if isinstance(value, dict):
            nested = check_payload(value)
            if len(nested.keys()) > 0:
                updated_payload[key] = nested
        elif value != '' and value is not None:
            updated_payload[key] = value
    return updated_payload


def get_assets(config, params):
    try:
        dg = Dragos(config)
        endpoint = 'assets/api/v4/getAssets'
        payload = {}
        pagination = {}
        maskAddressTimeRanges = {}
        overlapsAddressTimeRange = {}
        selector = {}
        # Handle pagination
        pagination_fields = ['pageNumber', 'pageSize', 'limitTotalCount', 'sort_by']
        for field in pagination_fields:
            value = params.get(field)
            if value:
                if field == 'sort_by':
                    # Build 'sorts' list based on 'sort_by' and 'order_by'
                    pagination['sorts'] = [
                        {"field": ASSET_SORT_BY.get(field), "descending": params.get('order_by', False)} for
                        field in value]
                else:
                    pagination[field] = value

        # Add pagination to payload if it contains any data
        if pagination:
            payload['pagination'] = pagination

        # Handle maskAddressTimeRanges
        maskAddress_starttime = params.get('maskAddress_starttime')
        maskAddress_endtime = params.get('maskAddress_endtime')
        if maskAddress_starttime and maskAddress_endtime:
            maskAddressTimeRanges['from'] = maskAddress_starttime
            maskAddressTimeRanges['to'] = maskAddress_endtime

        # Add maskAddressTimeRanges to payload if it contains any data
        if maskAddressTimeRanges:
            payload['maskAddressTimeRanges'] = maskAddressTimeRanges

        # Handle overlapsAddressTimeRange
        overlaps_starttime = params.get('overlaps_starttime')
        overlaps_endtime = params.get('overlaps_endtime')
        if overlaps_starttime and overlaps_endtime:
            overlapsAddressTimeRange['from'] = overlaps_starttime
            overlapsAddressTimeRange['to'] = overlaps_endtime

        # Add overlapsAddressTimeRange to payload if it contains any data
        if overlapsAddressTimeRange:
            payload['overlapsAddressTimeRange'] = overlapsAddressTimeRange

        # Handle created and lastseen datetime

        createdAtAfter = params.get('createdAtAfter')
        createdAtBefore = params.get('createdAtBefore')
        lastSeenAtAfter = params.get('lastSeenAtAfter')
        lastSeenAtBefore = params.get('lastSeenAtBefore')
        isDeleted = params.get('is_deleted')
        if createdAtAfter:
            selector['createdAtAfter'] = createdAtAfter
        if createdAtBefore:
            selector['createdAtBefore'] = createdAtBefore
        if lastSeenAtAfter:
            selector['lastSeenAtAfter'] = lastSeenAtAfter
        if lastSeenAtBefore:
            selector['lastSeenAtBefore'] = lastSeenAtBefore
        if isDeleted:
            selector['isDeleted'] = isDeleted

        # Add selector to payload if it contains any data
        if selector:
            payload['selector'] = selector

        additional_fields = params.get('additional_fields')
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload {0}".format(payload))
        response = dg.make_rest_call(endpoint, 'POST', data=json.dumps(payload))
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_notifications(config, params):
    try:
        dg = Dragos(config)
        endpoint = 'notifications/api/v2/notification'
        payload = {
            "pageNumber": params.get('pageNumber'),
            "pageSize": params.get('pageSize'),
            "offset": params.get('offset'),
            "filter": params.get('filter'),
            "resolveChildrenDepth": params.get('resolveChildrenDepth'),
            "sorts": params.get('sorts'),
            "sortField": NOTIFICATION_SORT.get(params.get('sortField')) if params.get('sortField') else "",
            "sortDescending": params.get('sortDescending'),
            "limitTotalCount": params.get('limitTotalCount')
        }
        additional_fields = params.get('additional_fields')
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload {0}".format(payload))
        response = dg.make_rest_call(endpoint, 'GET', params=payload)
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_notification_details(config, params):
    try:
        dg = Dragos(config)
        endpoint = 'notifications/api/v2/notification/batch'
        ids = params.get('ids')
        payload = {
            "ids": [int(id) for id in ids.split(",")] if type(ids) is str else ids,
            "includeConversations": params.get('includeConversations'),
            "resolveChildrenDepth": params.get('resolveChildrenDepth')
        }
        payload = check_payload(payload)
        logger.debug("Payload {0}".format(payload))
        response = dg.make_rest_call(endpoint, 'GET', params=payload)
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_stats_of_notification(config, params):
    try:
        dg = Dragos(config)
        endpoint = 'notifications/api/v2/notification/stats'
        payload = {
            "groupBy": ",".join(NOTIFICATION_GROUP_BY.get(field) for field in params.get('groupBy')),
            "filter": params.get('filter')
        }
        payload = check_payload(payload)
        logger.debug("Payload {0}".format(payload))
        response = dg.make_rest_call(endpoint, 'GET', params=payload)
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_vulnerabilities(config, params):
    try:
        dg = Dragos(config)
        endpoint = 'vulnerabilities/api/v1/vulnerability'
        payload = {}
        pagination = {}
        # Handle pagination
        pagination_fields = ['pageNumber', 'pageSize', 'limitTotalCount', 'sort_by']
        for field in pagination_fields:
            value = params.get(field)
            if value:
                if field == 'sort_by':
                    # Build 'sorts' list based on 'sort_by' and 'order_by'
                    pagination['sorts'] = [{"field": field, "descending": params.get('order_by', False)} for field in
                                           (value if isinstance(value, list) else value.split(","))]

                else:
                    pagination[field] = value

        # Add pagination to payload if it contains any data
        if pagination:
            payload['pagination'] = pagination
        additional_fields = params.get('additional_fields')
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload {0}".format(payload))
        response = dg.make_rest_call(endpoint, 'POST', data=json.dumps(payload))
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_vulnerability_detections(config, params):
    try:
        dg = Dragos(config)
        endpoint = 'vulnerabilities/api/v1/vulnerability/detection'
        payload = {}
        pagination = {}
        # Handle pagination
        pagination_fields = ['pageNumber', 'pageSize', 'limitTotalCount', 'sort_by']
        for field in pagination_fields:
            value = params.get(field)
            if value:
                if field == 'sort_by':
                    # Build 'sorts' list based on 'sort_by' and 'order_by'
                    pagination['sorts'] = [{"field": field, "descending": params.get('order_by', False)} for field in
                                           (value if isinstance(value, list) else value.split(","))]
                else:
                    pagination[field] = value

        # Add pagination to payload if it contains any data
        if pagination:
            payload['pagination'] = pagination
        additional_fields = params.get('additional_fields')
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload {0}".format(payload))
        response = dg.make_rest_call(endpoint, 'POST', data=json.dumps(payload))
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def get_detections(config, params):
    try:
        dg = Dragos(config)
        endpoint = 'detections/api/v2/detections/search'
        payload = {}
        view = {}
        pagination = {}
        # Handle pagination
        pagination_fields = ['pageNumber', 'pageSize', 'limitTotalCount', 'sort_by']
        for field in pagination_fields:
            value = params.get(field)
            if value:
                if field == 'sort_by':
                    # Build 'sorts' list based on 'sort_by' and 'order_by'
                    pagination['sorts'] = [{"field": field, "descending": params.get('order_by', False)} for field in
                                           (value if isinstance(value, list) else value.split(","))]
                else:
                    pagination[field] = value

        # Add pagination to payload if it contains any data
        if pagination:
            payload['pagination'] = pagination

        # Handle View
        includeFields = params.get('includeFields')
        if includeFields:
            view['includeFields'] = includeFields if isinstance(includeFields, list) else includeFields.split(",")
        excludeFields = params.get('excludeFields')
        if excludeFields:
            view['excludeFields'] = excludeFields if isinstance(excludeFields, list) else excludeFields.split(",")
        # Add view to payload if it contains any data
        if view:
            payload['view'] = view
        additional_fields = params.get('additional_fields')
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload {0}".format(payload))
        response = dg.make_rest_call(endpoint, 'POST', data=json.dumps(payload))
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def execute_an_api_call(config, params):
    try:
        dg = Dragos(config)
        endpoint = params.get("endpoint")
        http_method = params.get("method")
        query_params = params.get("query_params") if params.get("query_params") else None
        payload = json.dumps(params.get("payload")) if params.get("payload") else None
        logger.debug("Payload: {0}".format(payload))
        response = dg.make_rest_call(endpoint, method=http_method, params=query_params, data=json.dumps(payload))
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def check_health(config):
    try:
        response = get_assets(config, params={'pageSize': 1})
        if response:
            return True
    except Exception as err:
        logger.info(str(err))
        raise ConnectorError(str(err))


operations = {
    'get_assets': get_assets,
    'get_notifications': get_notifications,
    'get_notification_details': get_notification_details,
    'get_stats_of_notification': get_stats_of_notification,
    'get_vulnerabilities': get_vulnerabilities,
    'get_vulnerability_detections': get_vulnerability_detections,
    'get_detections': get_detections,
    'execute_an_api_call': execute_an_api_call
}
