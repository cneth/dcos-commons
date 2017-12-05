import pytest

import sdk_cmd
import sdk_fault_domain
import sdk_install
import sdk_tasks
import sdk_utils

from tests import config


@pytest.mark.sanity
@pytest.mark.dcos_min_version('1.11')
def test_detect_zones_disabled_by_default():
    foldered_name = sdk_utils.get_foldered_name(config.SERVICE_NAME)

    sdk_install.uninstall(config.PACKAGE_NAME, foldered_name)
    sdk_install.install(
        config.PACKAGE_NAME,
        foldered_name,
        config.DEFAULT_BROKER_COUNT,
        additional_options={
            "service": {
                "name": foldered_name
            }
        })

    broker_ids = sdk_cmd.svc_cli(
        config.PACKAGE_NAME, foldered_name, 'broker list', json=True)

    for broker_id in broker_ids:
        broker_info = sdk_cmd.svc_cli(
            config.PACKAGE_NAME,
            foldered_name,
            'broker get {}'.format(broker_id),
            json=True)

        assert broker_info.get('rack') == None

    sdk_install.uninstall(config.PACKAGE_NAME, foldered_name)


@pytest.mark.sanity
@pytest.mark.dcos_min_version('1.11')
def test_detect_zones_enabled():
    foldered_name = sdk_utils.get_foldered_name(config.SERVICE_NAME)

    sdk_install.uninstall(config.PACKAGE_NAME, foldered_name)
    sdk_install.install(
        config.PACKAGE_NAME,
        foldered_name,
        config.DEFAULT_BROKER_COUNT,
        additional_options={
            "service": {
                "name": foldered_name,
                "detect_zones": True
            }
        })

    broker_ids = sdk_cmd.svc_cli(
        config.PACKAGE_NAME, foldered_name, 'broker list', json=True)

    for broker_id in broker_ids:
        broker_info = sdk_cmd.svc_cli(
            config.PACKAGE_NAME,
            foldered_name,
            'broker get {}'.format(broker_id),
            json=True)

        assert sdk_fault_domain.is_valid_zone(broker_info.get('rack'))

        sdk_install.uninstall(config.PACKAGE_NAME, foldered_name)
