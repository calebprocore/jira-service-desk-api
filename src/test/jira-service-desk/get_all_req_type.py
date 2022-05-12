import json
import os
import requests
from base.config import Config


class JiraServiceDesk(object):
    """
    status: now working

    # --
    When running this, the top level project directory has to be the base working directory,
    as it needs to find 'config/dev.ini' relative to there to get API keys.

    <path>/jira-service-desk-api/ has to be the base working directory

    $cd jira-service-desk-api
    $python src/test/jira-service-desk/get_all_req_type.py
    """

    def __init__(self):
        self.config = None
        self.auth = None

        self.jira_rum_service_desk_id = None
        self.jira_rum_request_type_id = None

        self.jira_host = None
        self.jira_user = None
        self.jira_api_token = None
        self.jira_user_api_token = None  # $user:api_token
        self.jira_base64_user_api_token = None  # Base64Encoded($user:api_token)

    def init(self):
        self.config = Config()
        self.config.init()
        self.read_params()

    def read_params(self):
        try:
            self.jira_host = self.config.get_value(
                'JIRA', 'JIRA_HOST')

            self.jira_rum_service_desk_id = self.config.get_value(
                'JIRA',
                'JIRA_RUM_SERVICE_DESK_ID')

            self.jira_rum_request_type_id = self.config.get_value(
                'JIRA', 'JIRA_RUM_REQUEST_TYPE_ID')

            self.jira_user = self.config.get_value('JIRA', 'JIRA_USER')
            self.jira_api_token = self.config.get_value('JIRA', 'JIRA_API_TOKEN')

            self.jira_user_api_token = self.jira_user + ':' + self.jira_api_token
            self.jira_base64_user_api_token = self.config.get_value(
                'JIRA',
                'JIRA_BASE64_USER_API_TOKEN')

            print('jira_host: ' + self.jira_host)
            print('jira_rum_service_desk_id: ' + self.jira_rum_service_desk_id)
            print('jira_rum_request_type_id: ' + self.jira_rum_request_type_id)

        except Exception as e__read_params:
            print('Exception:', e__read_params, flush=True)
        finally:
            self.jira_host = self.config.get_value('JIRA', 'JIRA_HOST')

    def get_headers(self):
        accept_content_type = 'application/json'
        headers = {
            'User-Agent': 'python-requests',
            'X-ExperimentalApi': 'opt-in',
            'Authorization': 'Basic ' + self.jira_base64_user_api_token,
            'Content-Type': accept_content_type,
            'Accept': accept_content_type
        }
        # 'Authorization': 'Bearer ' + self.jira_user_api_token,
        return headers

        # the following Authorization methods **do NOT work**
        # 'Authorization': 'Bearer ' + self.jira_base64_user_api_token  | Base64Encoded(user:api_token)
        # 'Authorization': 'Basic ' + self.jira_base64_user_api_token   | Base64Encoded(user:api_token)
        # 'Authorization': 'Basic ' + self.jira_user_api_token          | user:api_token
        # 'Authorization': 'Bearer ' + self.jira_user_api_token         | user:api_token

        # errors:
        # Basic:    Basic authentication with passwords is deprecated. (I'm not using a password)
        # Bearer:   {"message": "Client must be authenticated to access this resource.
        # status-code": 401}

    def get_all_req_type(self):
        url = self.jira_host + '/rest/servicedeskapi/requesttype'
        headers = self.get_headers()
        r = requests.get(url, headers=headers)
        # r = requests.post(url, headers=headers) # todo, catch error on post, method not allowed
        print(r.text)

    def main(self):
        self.init()  # read all params from dev.ini
        self.get_all_req_type()


if __name__ == '__main__':
    this_class = 'JiraServiceDesk'
    c = None
    try:
        c = JiraServiceDesk()
        c.main()
    except Exception as e__main:
        print('Exception:', e__main, flush=True)
    finally:
        pass
