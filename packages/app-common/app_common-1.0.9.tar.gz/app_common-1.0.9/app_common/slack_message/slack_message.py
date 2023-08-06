import json

from urllib import request

SLACK_MESSAGE_COLOR_GREEN = "good"
SLACK_MESSAGE_COLOR_RED = "danger"
SLACK_WEB_HOOK_BASE_URL = "https://hooks.slack.com/services/"

SUCCEEDED = "Succeeded"
FAILED = "Failed"


class SlackMessenger:
    SUCCEEDED = SUCCEEDED
    FAILED = FAILED

    def __init__(self, slack_token=None, project_name=None, channel=None):
        self.slack_token = slack_token
        self.project_name = project_name
        self.channel = channel

    def _set_up_checking(self):
        if any([not self.channel, not self.slack_token, not self.project_name]):
            raise ValueError("Has to set up the slack message before sending message")

    def set_up(self, slack_token, project_name, channel):
        self.slack_token = slack_token
        self.project_name = project_name
        self.channel = channel

    def send_success_message(self, job_name, detail, title=None, text=None, channel=None):
        self._set_up_checking()
        self.send_message(job_name, detail, title=title, text=text, channel=channel)

    def send_fail_message(self, job_name, detail, title=None, text=None, channel=None):
        self._set_up_checking()
        self.send_message(job_name, detail, status=FAILED, title=title, text=text, channel=channel)

    def send_message(self, job_name, detail, status=SUCCEEDED, title=None, text=None, channel=None):
        sending_dict = self.text_dict_maker(job_name, status, detail, title=title, text=text, channel=channel)
        self._sending_message(sending_dict)

    def _sending_message(self, text_dict):
        post = text_dict
        try:
            json_data = json.dumps(post)
            req = request.Request(SLACK_WEB_HOOK_BASE_URL + self.slack_token,
                                  data=json_data.encode('ascii'),
                                  headers={'Content-Type': 'application/json'})
            resp = request.urlopen(req)
        except Exception as em:
            print("EXCEPTION: " + str(em))

    def text_dict_maker(self, job_name, status, detail, title=None, text=None, channel=None):
        if status == SUCCEEDED:
            color = SLACK_MESSAGE_COLOR_GREEN
        elif status == FAILED:
            color = SLACK_MESSAGE_COLOR_RED
        else:
            msg = "status code should be either {} or {}".format(SUCCEEDED, FAILED)
            raise ValueError(msg)
        if channel:
            channel = channel
        else:
            channel = self.channel
        sending_dict = {
            "channel": channel,
            "attachments": [
                {
                    "fallback": "This message was sent from {} project".format(self.project_name),
                    "color": color,
                    "title": title,
                    "text": "",
                    "fields": [
                        {
                            "title": "Job Name",
                            "value": job_name,
                            "short": True
                        },
                        {
                            "title": "Project",
                            "value": self.project_name,
                            "short": True,
                        },
                        {
                            "title": "Status",
                            "value": status,
                            "short": True
                        },
                        {
                            "title": "Detail",
                            "value": detail,
                            "short": True
                        }
                    ]
                }
            ]
        }
        if title:
            sending_dict["attachments"][0]["title"] = title
        if text:
            sending_dict["attachments"][0]["text"] = text
        return sending_dict
