# Edit the config_and_params.json file and add the required parameter values.
# Add any specific assertions in each test case, based on the expected response.
# Add logic for validating conditional_output_schema.

"""
Copyright start
MIT License
Copyright (c) 2025 Fortinet Inc
Copyright end
"""

import pytest
from pprint import pformat
from testframework.conftest import initial_setup, info_json, params_json, validate_params, connector_id, connector_details,\
    valid_configuration, invalid_configuration, valid_configuration_with_token, conn_cleanup
from testframework.helpers.test_helpers import run_health_check_success, run_invalid_config_test, run_success_test,\
    run_output_schema_validation, run_invalid_param_test, set_report_metadata
from testframework.helpers.test_constants import VALID_CONFIG_TITLE, VALID_INPUT_TITLE, INVALID_PARAM_TITLE,\
    SCHEMA_VALIDATION_TITLE, STATUS_MISMATCH_ERROR
    

@pytest.mark.check_health
@pytest.mark.success
def test_check_health_success(valid_configuration, connector_details):
    set_report_metadata(connector_details, "Health Check", VALID_CONFIG_TITLE)
    result = run_health_check_success(valid_configuration, connector_details)
    assert result.get('status', '').lower() == 'available',\
        STATUS_MISMATCH_ERROR.format(expected='available', result=pformat(result))
    

@pytest.mark.check_health
@pytest.mark.invalid_input
def test_check_health_invalid_server_url(invalid_configuration, connector_id, connector_details, params_json):
    set_report_metadata(connector_details, "Health Check", INVALID_PARAM_TITLE.format(param='Server URL'))
    result = run_invalid_config_test(invalid_configuration, connector_id, connector_details, param_name='server_url',
                                     param_type='text', config=params_json['config'])
    assert result.get('status', '').lower() == "disconnected",\
        STATUS_MISMATCH_ERROR.format(expected='disconnected', result=pformat(result))
    

@pytest.mark.check_health
@pytest.mark.invalid_input
def test_check_health_invalid_api_secret(invalid_configuration, connector_id, connector_details, params_json):
    set_report_metadata(connector_details, "Health Check", INVALID_PARAM_TITLE.format(param='API Secret'))
    result = run_invalid_config_test(invalid_configuration, connector_id, connector_details, param_name='api_secret',
                                     param_type='password', config=params_json['config'])
    assert result.get('status', '').lower() == "disconnected",\
        STATUS_MISMATCH_ERROR.format(expected='disconnected', result=pformat(result))
    

@pytest.mark.check_health
@pytest.mark.invalid_input
def test_check_health_invalid_api_id(invalid_configuration, connector_id, connector_details, params_json):
    set_report_metadata(connector_details, "Health Check", INVALID_PARAM_TITLE.format(param='API ID'))
    result = run_invalid_config_test(invalid_configuration, connector_id, connector_details, param_name='api_id',
                                     param_type='password', config=params_json['config'])
    assert result.get('status', '').lower() == "disconnected",\
        STATUS_MISMATCH_ERROR.format(expected='disconnected', result=pformat(result))
    

@pytest.mark.get_assets
@pytest.mark.success
def test_get_assets_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Assets", VALID_INPUT_TITLE)
    for result in run_success_test(cache, connector_details, operation_name='get_assets',
                                   action_params=params_json['get_assets']):
        assert result.get('status') == "Success",\
            STATUS_MISMATCH_ERROR.format(expected='Success', result=pformat(result))


@pytest.mark.get_assets
@pytest.mark.schema_validation
def test_validate_get_assets_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get All Assets", SCHEMA_VALIDATION_TITLE)
    run_output_schema_validation(cache, 'get_assets', info_json, params_json['get_assets'])
    

@pytest.mark.get_assets
@pytest.mark.invalid_input
def test_get_assets_invalid_pagenumber(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Assets", INVALID_PARAM_TITLE.format(param='pageNumber'))
    result = run_invalid_param_test(connector_details, operation_name='get_assets', param_name='pageNumber',
                                    param_type='integer', action_params=params_json['get_assets'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_assets
@pytest.mark.invalid_input
def test_get_assets_invalid_additional_fields(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Assets", INVALID_PARAM_TITLE.format(param='Additional Parameters'))
    result = run_invalid_param_test(connector_details, operation_name='get_assets', param_name='additional_fields',
                                    param_type='json', action_params=params_json['get_assets'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_assets
@pytest.mark.invalid_input
def test_get_assets_invalid_is_deleted(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Assets", INVALID_PARAM_TITLE.format(param='Is Deleted'))
    result = run_invalid_param_test(connector_details, operation_name='get_assets', param_name='is_deleted',
                                    param_type='text', action_params=params_json['get_assets'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_assets
@pytest.mark.invalid_input
def test_get_assets_invalid_limittotalcount(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Assets", INVALID_PARAM_TITLE.format(param='Limit Total Count'))
    result = run_invalid_param_test(connector_details, operation_name='get_assets', param_name='limitTotalCount',
                                    param_type='integer', action_params=params_json['get_assets'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_assets
@pytest.mark.invalid_input
def test_get_assets_invalid_pagesize(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Assets", INVALID_PARAM_TITLE.format(param='PageSize'))
    result = run_invalid_param_test(connector_details, operation_name='get_assets', param_name='pageSize',
                                    param_type='integer', action_params=params_json['get_assets'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_notifications
@pytest.mark.success
def test_get_notifications_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Notifications", VALID_INPUT_TITLE)
    for result in run_success_test(cache, connector_details, operation_name='get_notifications',
                                   action_params=params_json['get_notifications']):
        assert result.get('status') == "Success",\
            STATUS_MISMATCH_ERROR.format(expected='Success', result=pformat(result))


@pytest.mark.get_notifications
@pytest.mark.schema_validation
def test_validate_get_notifications_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get All Notifications", SCHEMA_VALIDATION_TITLE)
    run_output_schema_validation(cache, 'get_notifications', info_json, params_json['get_notifications'])


@pytest.mark.get_notifications
@pytest.mark.invalid_input
def test_get_notifications_invalid_sorts(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Notifications", INVALID_PARAM_TITLE.format(param='Sorts'))
    result = run_invalid_param_test(connector_details, operation_name='get_notifications', param_name='sorts',
                                    param_type='text', action_params=params_json['get_notifications'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_notifications
@pytest.mark.invalid_input
def test_get_notifications_invalid_filter(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Notifications", INVALID_PARAM_TITLE.format(param='Filter'))
    result = run_invalid_param_test(connector_details, operation_name='get_notifications', param_name='filter',
                                    param_type='text', action_params=params_json['get_notifications'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_notifications
@pytest.mark.invalid_input
def test_get_notifications_invalid_limittotalcount(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Notifications", INVALID_PARAM_TITLE.format(param='Limit Total Count'))
    result = run_invalid_param_test(connector_details, operation_name='get_notifications', param_name='limitTotalCount',
                                    param_type='integer', action_params=params_json['get_notifications'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_notification_details
@pytest.mark.success
def test_get_notification_details_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Notifications Details", VALID_INPUT_TITLE)
    for result in run_success_test(cache, connector_details, operation_name='get_notification_details',
                                   action_params=params_json['get_notification_details']):
        assert result.get('status') == "Success",\
            STATUS_MISMATCH_ERROR.format(expected='Success', result=pformat(result))


@pytest.mark.get_notification_details
@pytest.mark.schema_validation
def test_validate_get_notification_details_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Notifications Details", SCHEMA_VALIDATION_TITLE)
    run_output_schema_validation(cache, 'get_notification_details', info_json, params_json['get_notification_details'])

    

@pytest.mark.get_notification_details
@pytest.mark.invalid_input
def test_get_notification_details_invalid_ids(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Notifications Details", INVALID_PARAM_TITLE.format(param='Notification IDs'))
    result = run_invalid_param_test(connector_details, operation_name='get_notification_details', param_name='ids',
                                    param_type='text', action_params=params_json['get_notification_details'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_stats_of_notification
@pytest.mark.success
def test_get_stats_of_notification_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Statistics of Notification", VALID_INPUT_TITLE)
    for result in run_success_test(cache, connector_details, operation_name='get_stats_of_notification',
                                   action_params=params_json['get_stats_of_notification']):
        assert result.get('status') == "Success",\
            STATUS_MISMATCH_ERROR.format(expected='Success', result=pformat(result))


@pytest.mark.get_stats_of_notification
@pytest.mark.schema_validation
def test_validate_get_stats_of_notification_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get Statistics of Notification", SCHEMA_VALIDATION_TITLE)
    run_output_schema_validation(cache, 'get_stats_of_notification', info_json, params_json['get_stats_of_notification'])
    

@pytest.mark.get_stats_of_notification
@pytest.mark.invalid_input
def test_get_stats_of_notification_invalid_filter(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get Statistics of Notification", INVALID_PARAM_TITLE.format(param='Filter'))
    result = run_invalid_param_test(connector_details, operation_name='get_stats_of_notification', param_name='filter',
                                    param_type='text', action_params=params_json['get_stats_of_notification'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_vulnerabilities
@pytest.mark.success
def test_get_vulnerabilities_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerabilities", VALID_INPUT_TITLE)
    for result in run_success_test(cache, connector_details, operation_name='get_vulnerabilities',
                                   action_params=params_json['get_vulnerabilities']):
        assert result.get('status') == "Success",\
            STATUS_MISMATCH_ERROR.format(expected='Success', result=pformat(result))


@pytest.mark.get_vulnerabilities
@pytest.mark.schema_validation
def test_validate_get_vulnerabilities_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get All Vulnerabilities", SCHEMA_VALIDATION_TITLE)
    run_output_schema_validation(cache, 'get_vulnerabilities', info_json, params_json['get_vulnerabilities'])
    

@pytest.mark.get_vulnerabilities
@pytest.mark.invalid_input
def test_get_vulnerabilities_invalid_pagenumber(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerabilities", INVALID_PARAM_TITLE.format(param='pageNumber'))
    result = run_invalid_param_test(connector_details, operation_name='get_vulnerabilities', param_name='pageNumber',
                                    param_type='integer', action_params=params_json['get_vulnerabilities'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_vulnerabilities
@pytest.mark.invalid_input
def test_get_vulnerabilities_invalid_additional_fields(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerabilities", INVALID_PARAM_TITLE.format(param='Additional Parameters'))
    result = run_invalid_param_test(connector_details, operation_name='get_vulnerabilities', param_name='additional_fields',
                                    param_type='json', action_params=params_json['get_vulnerabilities'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_vulnerabilities
@pytest.mark.invalid_input
def test_get_vulnerabilities_invalid_limittotalcount(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerabilities", INVALID_PARAM_TITLE.format(param='Limit Total Count'))
    result = run_invalid_param_test(connector_details, operation_name='get_vulnerabilities', param_name='limitTotalCount',
                                    param_type='integer', action_params=params_json['get_vulnerabilities'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_vulnerabilities
@pytest.mark.invalid_input
def test_get_vulnerabilities_invalid_sort_by(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerabilities", INVALID_PARAM_TITLE.format(param='Sort By'))
    result = run_invalid_param_test(connector_details, operation_name='get_vulnerabilities', param_name='sort_by',
                                    param_type='text', action_params=params_json['get_vulnerabilities'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_vulnerabilities
@pytest.mark.invalid_input
def test_get_vulnerabilities_invalid_pagesize(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerabilities", INVALID_PARAM_TITLE.format(param='PageSize'))
    result = run_invalid_param_test(connector_details, operation_name='get_vulnerabilities', param_name='pageSize',
                                    param_type='integer', action_params=params_json['get_vulnerabilities'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_vulnerability_detections
@pytest.mark.success
def test_get_vulnerability_detections_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerability Detections", VALID_INPUT_TITLE)
    for result in run_success_test(cache, connector_details, operation_name='get_vulnerability_detections',
                                   action_params=params_json['get_vulnerability_detections']):
        assert result.get('status') == "Success",\
            STATUS_MISMATCH_ERROR.format(expected='Success', result=pformat(result))


@pytest.mark.get_vulnerability_detections
@pytest.mark.schema_validation
def test_validate_get_vulnerability_detections_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get All Vulnerability Detections", SCHEMA_VALIDATION_TITLE)
    run_output_schema_validation(cache, 'get_vulnerability_detections', info_json, params_json['get_vulnerability_detections'])
    

@pytest.mark.get_vulnerability_detections
@pytest.mark.invalid_input
def test_get_vulnerability_detections_invalid_pagenumber(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerability Detections", INVALID_PARAM_TITLE.format(param='pageNumber'))
    result = run_invalid_param_test(connector_details, operation_name='get_vulnerability_detections', param_name='pageNumber',
                                    param_type='integer', action_params=params_json['get_vulnerability_detections'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_vulnerability_detections
@pytest.mark.invalid_input
def test_get_vulnerability_detections_invalid_additional_fields(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerability Detections", INVALID_PARAM_TITLE.format(param='Additional Parameters'))
    result = run_invalid_param_test(connector_details, operation_name='get_vulnerability_detections', param_name='additional_fields',
                                    param_type='json', action_params=params_json['get_vulnerability_detections'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_vulnerability_detections
@pytest.mark.invalid_input
def test_get_vulnerability_detections_invalid_limittotalcount(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerability Detections", INVALID_PARAM_TITLE.format(param='Limit Total Count'))
    result = run_invalid_param_test(connector_details, operation_name='get_vulnerability_detections', param_name='limitTotalCount',
                                    param_type='integer', action_params=params_json['get_vulnerability_detections'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_vulnerability_detections
@pytest.mark.invalid_input
def test_get_vulnerability_detections_invalid_sort_by(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerability Detections", INVALID_PARAM_TITLE.format(param='Sort By'))
    result = run_invalid_param_test(connector_details, operation_name='get_vulnerability_detections', param_name='sort_by',
                                    param_type='text', action_params=params_json['get_vulnerability_detections'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_vulnerability_detections
@pytest.mark.invalid_input
def test_get_vulnerability_detections_invalid_pagesize(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Vulnerability Detections", INVALID_PARAM_TITLE.format(param='PageSize'))
    result = run_invalid_param_test(connector_details, operation_name='get_vulnerability_detections', param_name='pageSize',
                                    param_type='integer', action_params=params_json['get_vulnerability_detections'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_detections
@pytest.mark.success
def test_get_detections_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Detections", VALID_INPUT_TITLE)
    for result in run_success_test(cache, connector_details, operation_name='get_detections',
                                   action_params=params_json['get_detections']):
        assert result.get('status') == "Success",\
            STATUS_MISMATCH_ERROR.format(expected='Success', result=pformat(result))


@pytest.mark.get_detections
@pytest.mark.schema_validation
def test_validate_get_detections_output_schema(cache, valid_configuration_with_token, connector_details,
                                                 info_json, params_json):
    set_report_metadata(connector_details, "Get All Detections", SCHEMA_VALIDATION_TITLE)
    run_output_schema_validation(cache, 'get_detections', info_json, params_json['get_detections'])
    

@pytest.mark.get_detections
@pytest.mark.invalid_input
def test_get_detections_invalid_pagenumber(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Detections", INVALID_PARAM_TITLE.format(param='pageNumber'))
    result = run_invalid_param_test(connector_details, operation_name='get_detections', param_name='pageNumber',
                                    param_type='integer', action_params=params_json['get_detections'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_detections
@pytest.mark.invalid_input
def test_get_detections_invalid_additional_fields(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Detections", INVALID_PARAM_TITLE.format(param='Additional Parameters'))
    result = run_invalid_param_test(connector_details, operation_name='get_detections', param_name='additional_fields',
                                    param_type='json', action_params=params_json['get_detections'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_detections
@pytest.mark.invalid_input
def test_get_detections_invalid_limittotalcount(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Detections", INVALID_PARAM_TITLE.format(param='Limit Total Count'))
    result = run_invalid_param_test(connector_details, operation_name='get_detections', param_name='limitTotalCount',
                                    param_type='integer', action_params=params_json['get_detections'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_detections
@pytest.mark.invalid_input
def test_get_detections_invalid_sort_by(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Detections", INVALID_PARAM_TITLE.format(param='Sort By'))
    result = run_invalid_param_test(connector_details, operation_name='get_detections', param_name='sort_by',
                                    param_type='text', action_params=params_json['get_detections'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.get_detections
@pytest.mark.invalid_input
def test_get_detections_invalid_pagesize(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Get All Detections", INVALID_PARAM_TITLE.format(param='PageSize'))
    result = run_invalid_param_test(connector_details, operation_name='get_detections', param_name='pageSize',
                                    param_type='integer', action_params=params_json['get_detections'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.execute_an_api_call
@pytest.mark.success
def test_execute_an_api_call_success(cache, valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Execute an API Request", VALID_INPUT_TITLE)
    for result in run_success_test(cache, connector_details, operation_name='execute_an_api_call',
                                   action_params=params_json['execute_an_api_call']):
        assert result.get('status') == "Success",\
            STATUS_MISMATCH_ERROR.format(expected='Success', result=pformat(result))
    

@pytest.mark.execute_an_api_call
@pytest.mark.invalid_input
def test_execute_an_api_call_invalid_query_params(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Execute an API Request", INVALID_PARAM_TITLE.format(param='Query Parameters'))
    result = run_invalid_param_test(connector_details, operation_name='execute_an_api_call', param_name='query_params',
                                    param_type='json', action_params=params_json['execute_an_api_call'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    

@pytest.mark.execute_an_api_call
@pytest.mark.invalid_input
def test_execute_an_api_call_invalid_endpoint(valid_configuration_with_token, connector_details, params_json):
    set_report_metadata(connector_details, "Execute an API Request", INVALID_PARAM_TITLE.format(param='Endpoint'))
    result = run_invalid_param_test(connector_details, operation_name='execute_an_api_call', param_name='endpoint',
                                    param_type='text', action_params=params_json['execute_an_api_call'])
    assert result.get('status') == "failed",\
        STATUS_MISMATCH_ERROR.format(expected='failed', result=pformat(result))
    
