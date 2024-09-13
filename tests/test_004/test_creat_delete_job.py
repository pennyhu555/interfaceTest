from jenkins import Jenkins
import pytest

admin = Jenkins('http://47.115.133.87:8080', 'admin',
                    '1114f9db70dac50a1b30197718c5671c86')
anonymous = Jenkins('http://47.115.133.87:8080')


def test_create_and_delete_jobs():
    job_dsl = """properties([parameters([string(name: 'Run', defaultValue: 'Yes', description: 'a parameter')])])node {stage("test"){echo 'Hello World'}}"""
    r1 = admin.create_job_with_dsl(job_dsl, "testjob0001")
    print(r1)
    r2 = admin.create_job_with_dsl(job_dsl, "testjob0002")
    print(r2)
    r = admin.delete_all_jobs()

    
if __name__ == '__main__':
    pytest.main(['-s'])
