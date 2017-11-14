#This is a script to help with the emailing of speakers from an email account

from __future__ import print_function
import httplib2
import os

#from apiclient import discovery
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from email.mime import text 
import base64

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'gmail_client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = text.MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw = base64.urlsafe_b64encode(message.as_bytes()) 
  raw = raw.decode()
  return {'raw': raw}
  #return {'raw': base64.urlsafe_b64encode(message.as_string())}
  #return {'raw': base64.urlsafe_b64encode(message.as_bytes())}
  #return {'raw': base64.urlsafe_b64encode(str.encode(message.as_string()))}



def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except:
   # print('An error occurred:{}'.format(error))
    print('OOPS!')


def send_email(email_address, facebook_video_link):
    """
    email_address : The recipenent of the email
    facebook_video_link : The video link for the video
    """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    #message = create_message('talkbot@websummit.com',email_address,
    #'Your Web Summit talk is live on Favebook', 'Hello!\nPlease find the link to your talk at Web Summit below \n {}'.format(facebook_video_link))

    
    message = create_message('talkbot@websummit.com',email_address,
    'Video of your talk', """Good news! We’ve edited down a video of your talk, which some might say is now perfect for sharing. Want to share your talk with your network? You can find your edited video here {}.""" .format(facebook_video_link))

    message = send_message(service,'talkbot@websummit.com',message)
    
    return message 

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    message = create_message('talkbot@websummit.com','aaron.meagher@cilabs.com',
    'Test of gmail api sending SUBJECT', 'Test of gmail api sending  \n and the new line \n www.facebook.com')

    send_message(service,'talkbot@websummit.com',message)




if __name__ == '__main__':
    send_email('test@websummit.com','blah blah blah')
    #get_credentials()