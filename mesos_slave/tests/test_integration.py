# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import platform

import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException
from datadog_checks.mesos_slave import MesosSlave

# Linux only: https://github.com/docker/for-mac/issues/1031
pytest.mark.skipif(platform.system() != 'Linux', reason="Only runs on Unix systems")


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_service_check(bad_instance, aggregator):
    check = MesosSlave('mesos_slave', {}, [bad_instance])

    with pytest.raises(CheckException):
        check.check(bad_instance)

    aggregator.assert_service_check('mesos_slave.can_connect', count=1, status=AgentCheck.CRITICAL)
