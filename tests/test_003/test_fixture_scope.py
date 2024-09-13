import pytest


@pytest.fixture(scope='session')
def simple_setup():
    print("\n test_fixture_scope执行测试+1")
    return 5


def test_1(simple_setup):
    assert simple_setup == 5


def test_2(simple_setup):
    assert simple_setup == 5


def test_3(simple_setup):
    assert simple_setup == 5


if __name__ == '__main__':
    pytest.main(['-s'])
