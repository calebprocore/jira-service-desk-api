import json
import requests
from base.config import Config


class JiraServiceDesk(object):
    """
    Jira: Service Desk Create Request

    Jira Service Desk API
    https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-servicedesk/

    Create Issue
    https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request/#api-rest-servicedeskapi-request-post

    config/dev.ini must be in place with the Jira API key
    to run, the current working directory must be the top level project directory so that this
    .py can find:   config/dev.ini relative.

    so:
    $python src/test/jira-service-desk-create_request.py

    will work

    In PyCharm, or other IDE, set 'working directory' to: <path>/jira-service-desk/
    """

    def __init__(self):
        self.config = None
        self.auth = None

        self.jira_rum_service_desk_id = None
        self.jira_rum_request_type_id = None

        self.jira_host = None
        self.jira_user = None
        self.jira_api_token = None
        self.jira_user_api_token = None
        self.jira_base64_user_api_token = None

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
        print('token:' + self.jira_user_api_token)
        headers = {
            'User-Agent': 'python-requests',
            'Authorization': 'Bearer ' + self.jira_user_api_token,
            'Content-Type': accept_content_type,
            'Accept': accept_content_type
        }

        # 1)
        # this does not work | Client must be authenticated to access this resource.
        # 'Authorization': 'Bearer ' + self.jira_base64_user_api_token,

        # 2)
        # this does not work | user:api_token | Client must be authenticated to access this
        # resource.
        # 'Authorization': 'Bearer ' + self.jira_user_api_token,

        # 3)
        # this does not work (basic deprecated)
        # 'Authorization': 'Basic ' + self.jira_user_api_token,

        # ---
        # The following Authorization methods **do NOT work**
        # 'Authorization': 'Bearer ' + self.jira_base64_user_api_token  | Base64Encoded(user:api_token)
        # 'Authorization': 'Basic ' + self.jira_base64_user_api_token   | Base64Encoded(user:api_token)
        # 'Authorization': 'Basic ' + self.jira_user_api_token          | user:api_token
        # 'Authorization': 'Bearer ' + self.jira_user_api_token         | user:api_token

        # errors:
        # Basic:    Basic authentication with passwords is deprecated. (I'm not using a password)
        # Bearer:   {"message": "Client must be authenticated to access this resource.
        # status-code": 401}
        return headers

    def submit_request(self):
        """
        Submit a request to Jira Service Desk
        """

        url = self.jira_host + '/rest/servicedeskapi/request'

        data = {
            "serviceDeskId": self.jira_rum_service_desk_id,
            "requestTypeId": self.jira_rum_request_type_id,
            "requestFieldValues": {
                "summary": "Jira Service Desk: request created via Python REST API",
                "description": "<description>"
            }
        }
        # "raiseOnBehalfOf": "?? email | jira_account_id"

        headers = self.get_headers()
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(r.text)

    def main(self):
        self.init()  # read and inspect Jira ID's needed for JSON payload
        self.submit_request()


if __name__ == '__main__':
    this_class = 'Jira'
    c = None
    try:
        c = JiraServiceDesk()
        c.main()
    except Exception as e__main:
        print('Exception:', e__main, flush=True)
    finally:
        pass
