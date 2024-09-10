class JenkinsJobAPI():
    def __init__(self, jenkins):
        self.jenkins = jenkins
        self.rest_client = jenkins.rest_client

    def list_jobs(self, attribute_to_show='name'):
        response = self.rest_client.get(f"/api/json?tree=jobs[{attribute_to_show}]")
        return response

    def get_job(self, job):
        response = self.rest_client.get(f"/job/{job}/api/json")
        return response

    def delete_job(self, job_name):
        response = self.rest_client.post(f"/job/{job_name}/doDelete")
        return response
