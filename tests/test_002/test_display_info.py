import pytest


def test_s1():
    print("不用-s执行的话，成功的测试日志不会打印")
    assert 5 == 5


def test_f1():
    print("不用-s执行的话，只有失败的测试才会打印出日志")
    assert 3 == 5


def test_answer():
    print("用-s执行的话，成功的测试日志会打印")


if __name__ == '__main__':
    pytest.main(['-s'])
    # pytest.main()
