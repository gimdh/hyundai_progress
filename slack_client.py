
import slack



class SlackClient:
    def __init__(self, oauth_token, ids):
        self.client = slack.WebClient(token=oauth_token)
        self.ids = ids

    
    def send_message(self, message):
        for id in self.ids:
            self.client.chat_postMessage(channel=id, text=message)

        
