import json
import requests
from base.config import Config


class JiraIssue(object):
    """
    Jira: Create Issue
    https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
    """

    def __init__(self):
        self.config = None

        self.jira_host = None
        self.jira_user = None
        self.jira_api_token = None
        self.jira_rum_prj_key = None
        self.jira_rum_issue_type_id = None

    def init(self):
        self.config = Config()
        self.config.init()
        self.read_params()

    def read_params(self):
        self.jira_host = self.config.get_value('JIRA', 'JIRA_HOST')
        self.jira_user = self.config.get_value('JIRA', 'JIRA_USER')
        self.jira_api_token = self.config.get_value('JIRA', 'JIRA_API_TOKEN')
        self.jira_rum_prj_key = self.config.get_value('JIRA', 'JIRA_RUM_PRJ_KEY')
        self.jira_rum_issue_type_id = self.config.get_value(
            'JIRA',
            'JIRA_RUM_REQUEST_ISSUE_TYPE_ID')

        print('jira_host: ' + self.jira_host)  # verify that is read by printing one value
        print('jira_rum_issue_type_id: ' + self.jira_rum_issue_type_id)
        # value

        # combine $USER:$TOKEN here to create 'user_api_token' to use in API call
        self.jira_user_api_token = self.jira_user + ':' + self.jira_api_token
        print('self.jira_user_api_token: ' + self.jira_user_api_token)

    def get_headers(self):
        accept_content_type = 'application/json'
        headers = {
            'User-Agent': 'python-requests',
            'Authorization': 'Basic ' + self.jira_user_api_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return headers

    def submit_issue(self):
        # url = self.jira_host + '/rest/api/latest/issue'
        url = self.jira_host + '/rest/api/2/issue'

        data = {
            "fields": {"project": {"key": self.jira_rum_prj_key},
                       "summary": "created by python requests using Jira REST API",
                       "description": "created by python requests using Jira REST API",
                       "issuetype": {"id": self.jira_rum_issue_type_id}
                       }
        }

        headers = self.get_headers()
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(r.text)

    def main(self):
        self.init()  # read config/dev.ini
        self.submit_issue()


if __name__ == '__main__':
    this_class = 'Jira'
    c = None
    try:
        c = JiraIssue()
        c.main()
    except Exception as e__main:
        print('Exception:', e__main, flush=True)
    finally:
        pass
