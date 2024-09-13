from jenkins import Jenkins
import pytest


# ##########这里是测试账号区域-----属于测试数据##########
admin = Jenkins('http://47.115.133.87:8080', 'admin', '1114f9db70dac50a1b30197718c5671c86')
anonymous = Jenkins('http://47.115.133.87:8080')


# ##########这里是跟测试紧密相关的一些公用方法##########
def get_user(user_to_get, login_user):
    actual_result = login_user.get_user(user_to_get)
    return actual_result


def check_get_user_result(actual_result, expected_status_code, user_to_get, expected_full_name):
    assert actual_result.code == expected_status_code
    if actual_result.code != 404:
        assert actual_result.body['absoluteUrl'] == 'http:////47.115.133.87:8080/user/' + user_to_get
        assert actual_result.body['fullName'] == expected_full_name


# ##########分割线以下是测试方法##########
def test_get_user_admin_by_admin():
    actual_result = get_user("test", admin)
    check_get_user_result(actual_result, 200, 'test', 'test')


def test_get_user_test_by_admin():
    actual_result = get_user("admin", admin)
    check_get_user_result(actual_result, 200, 'admin', 'admin')


def test_get_user_admin_by_anonymous():
    actual_result = get_user("test", anonymous)
    check_get_user_result(actual_result, 200, 'test', 'test')


def test_get_user_test_by_anonymous():
    actual_result = get_user("admin", anonymous)
    check_get_user_result(actual_result, 200, 'admin', 'admin')


def test_get_user_notexist_by_anonymous():
    actual_result = get_user("notexist", anonymous)
    check_get_user_result(actual_result, 404, None, None)


if __name__ == '__main__':
    pytest.main(['-s'])

