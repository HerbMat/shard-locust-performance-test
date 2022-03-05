from json import JSONDecodeError
from random import randint

from locust import HttpUser, task, between, constant, run_single_user


class FirstTest(HttpUser):
    # wait_time = between(1, 2)
    wait_time = constant(1)
    existing_sessions = []
    host = "http://localhost:8080"

    @task(5)
    def get_elements(self):
        length = len(self.existing_sessions)
        if length > 0:
            el = self.existing_sessions[randint(0, length-1)]["accountId"]
            self.client.get(f"/session?accountId={el}")
            # with self.client.get(f"/session?accountId={el}", catch_response=True) as response:
            #     try:
            #         body = response.json()
            #         print(f"Retrieved elements {len(body)}")
            #     except JSONDecodeError:
            #         response.failure("Response could not be decoded as JSON")
            #     except KeyError:
            #         response.failure("Response did not contain expected key 'greeting'")

    @task(2)
    def create_session(self):
        self.client.put("/session", json=self._create_session())
        # with self.client.put("/session", json=self._create_session(), catch_response=True) as response:
        #     if response.status_code == 200:
        #         print("Success Save")
        #     else:
        #         print("Fail Save")

    @task
    def delete_session(self):
        length = len(self.existing_sessions)
        if length > 0:
            el = self.existing_sessions.pop(randint(0, length - 1))
            # with self.client.delete(f"/session?accountId={el['accountId']}&deviceId={el['deviceId']}", catch_response=True) as response:
            self.client.delete(f"/session?accountId={el['accountId']}&deviceId={el['deviceId']}")
                # if response.status_code == 204:
                #     print("Success Delete")
                # else:
                #     print("Fail Delete")

    def _create_session(self):
        account_id = randint(1, 100000)
        device_id = randint(1, 100000)
        new_session = {"accountId": account_id, "deviceId": device_id}
        self.existing_sessions.append(new_session)

        return new_session


if __name__ == "__main__":
    run_single_user(FirstTest)
