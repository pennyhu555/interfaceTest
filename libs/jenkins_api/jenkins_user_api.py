class JenkinsUserAPI():
    def __init__(self, jenkins):
        self.jenkins = jenkins
        self.rest_client = jenkins.rest_client

    def get_user(self, username):
        response = self.rest_client.get(f"/user/{username}/api/json")
        return response

    def asynch_people(self):
        response = self.rest_client.post(f"/asynchPeople/api/json")
        return response
