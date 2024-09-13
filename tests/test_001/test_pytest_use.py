import pytest
from jenkins import Jenkins


def test_jenkins_get_user_by_admin():
    admin = Jenkins('http://47.115.133.87:8080', 'admin',
                    '1114f9db70dac50a1b30197718c5671c86')
    actual_result = admin.get_user("admin")
    assert actual_result.code == 200
    print(actual_result.body)
    assert actual_result.body["absoluteUrl"] == 'http://47.115.133.87:8080/user/admin'
    assert actual_result.body["fullName"] == "admin"


def test_jenkins_get_user_anonymous():
    anonymous = Jenkins('http://47.115.133.87:8080')
    actual_result = anonymous.get_user("test")
    assert actual_result.code == 403
    # assert actual_result.body["absoluteUrl"] == 'http://47.115.133.8080/user/test'
    # assert actual_result.body["fullName"] == "test"


if __name__ == '__main__':
    pytest.main()
