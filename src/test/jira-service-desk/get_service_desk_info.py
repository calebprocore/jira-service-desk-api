
import json
import requests
from base.config import Config


class JiraServiceDesk(object):

    def __init__(self):
        self.config = None
        self.auth = None

        self.jira_rum_service_desk_id = None
        self.jira_rum_request_type_id = None

        self.jira_host = None
        self.jira_user = None
        self.jira_api_token = None
        self.jira_user_api_token = None         # $user:api_token
        self.jira_base64_user_api_token = None  # Base64Encoded($user:api_token)

    def init(self):
        self.config = Config()
        self.config.init()
        self.read_params()

    def read_params(self):
        self.jira_host = self.config.get_value('JIRA', 'JIRA_HOST')
        self.jira_rum_service_desk_id = self.config.get_value('JIRA', 'JIRA_RUM_SERVICE_DESK_ID')
        self.jira_rum_request_type_id = self.config.get_value('JIRA', 'JIRA_RUM_REQUEST_TYPE_ID')
        self.jira_user = self.config.get_value('JIRA', 'JIRA_USER')
        self.jira_api_token = self.config.get_value('JIRA', 'JIRA_API_TOKEN')

        self.jira_user_api_token = self.jira_user + ':' + self.jira_api_token
        self.jira_base64_user_api_token = self.config.get_value(
            'JIRA',
            'JIRA_BASE64_USER_API_TOKEN')

        print('jira_host: ' + self.jira_host)
        print('jira_rum_service_desk_id: ' + self.jira_rum_service_desk_id)
        print('jira_rum_request_type_id: ' + self.jira_rum_request_type_id)

    def get_headers(self):
        accept_content_type = 'application/json'
        headers = {
            'User-Agent': 'python-requests',
            'Authorization': 'Bearer ' + self.jira_base64_user_api_token,
            'Content-Type': accept_content_type,
            'Accept': accept_content_type
        }
        return headers

    def get_service_desk_info(self):
        url = self.jira_host + '/rest/servicedeskapi/info'
        headers = self.get_headers()
        r = requests.get(url, headers=headers)
        # r = requests.post(url, headers=headers) # todo, catch error on post, method not allowed
        print(r.text)

    def main(self):
        self.init()  # read and inspect Jira ID's needed for JSON payload
        self.get_service_desk_info()


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
