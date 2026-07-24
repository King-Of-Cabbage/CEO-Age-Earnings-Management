import pytest


def pytest_addoption(parser):
    parser.addoption("--config", action="store", default=None, help="Local integration config path")


@pytest.fixture
def local_config(request):
    config = request.config.getoption("--config")
    if not config:
        pytest.skip("integration test requires --config")
    return config
