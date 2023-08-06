import pytest
import csv
import re

pytest_plugins = 'pytester'

def pytest_addoption(parser):
    group = parser.getgroup("testplan")
    group.addoption("--testplan",
                       action="store",
                       default=None,
                       help="生成包含测试元数据的CSV并退出，而不运行测试"
                   )


def pytest_collection_modifyitems(session, config, items):
    path = config.getoption('testplan')
    if path:
        with open(path, mode='w') as fd:
            writer = csv.writer(fd, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["title", "description", "markers"])

            for item in items:
                title = item.nodeid
                description = re.sub('\n\s+', '\n', item.obj.__doc__.strip())
                markers = ','.join([m.name for m in item.iter_markers()])
                writer.writerow([title, description, markers])

        pytest.exit(f"测试计划已生成: {path}")