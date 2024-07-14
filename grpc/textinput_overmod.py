# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sample that implements a text client for the Google Assistant Service."""

import os
import logging
import json

import click
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

ASSISTANTFOLDER = 'X:\\Projects\\Python\\Whatsapp\\Assistant\\'

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)

try:
    from . import (
        assistant_helpers,
        browser_helpers,
    )
except (SystemError, ImportError):
    import assistant_helpers
    import browser_helpers


ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5
PLAYING = embedded_assistant_pb2.ScreenOutConfig.PLAYING


class SampleTextAssistant(object):
    """Sample Assistant that supports text based conversations.

    Args:
      language_code: language for the conversation.
      device_model_id: identifier of the device model.
      device_id: identifier of the registered device instance.
      display: enable visual display of assistant response.
      channel: authorized gRPC channel for connection to the
        Google Assistant API.
      deadline_sec: gRPC deadline in seconds for Google Assistant API call.
    """

    def __init__(self, language_code, device_model_id, device_id,
                                display, channel, deadline_sec):
        self.language_code = language_code
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.conversation_state = None
        # Force reset of first conversation.
        self.is_new_conversation = True
        self.display = display
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(
            channel
        )
        self.deadline = deadline_sec

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if e:
            return False

    def assist1(self, text_query):
        """Send a text request to the Assistant and playback the response.
        """
        def iter_assist_requests():
            config = embedded_assistant_pb2.AssistConfig(
                audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                    encoding='LINEAR16',
                    sample_rate_hertz=16000,
                    volume_percentage=0,
                ),
                dialog_state_in=embedded_assistant_pb2.DialogStateIn(
                    language_code=self.language_code,
                    conversation_state=self.conversation_state,
                    is_new_conversation=self.is_new_conversation,
                ),
                device_config=embedded_assistant_pb2.DeviceConfig(
                    device_id=self.device_id,
                    device_model_id=self.device_model_id,
                ),
                text_query=text_query,
            )
            # Continue current conversation with later requests.
            self.is_new_conversation = False
            if self.display:
                config.screen_out_config.screen_mode = PLAYING

            req = embedded_assistant_pb2.AssistRequest(config=config)
            assistant_helpers.log_assist_request_without_audio(req)
            yield req

        text_response = None
        html_response = None
        for resp in self.assistant.Assist(iter_assist_requests(),
                                          self.deadline):
            assistant_helpers.log_assist_response_without_audio(resp)
            if resp.screen_out.data:
                html_response = resp.screen_out.data
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                self.conversation_state = conversation_state
            if resp.dialog_state_out.supplemental_display_text:
                text_response = resp.dialog_state_out.supplemental_display_text
        return text_response, html_response

    def assist2(self, text_query):
        """Send a text request to the Assistant and playback the response.
        """
        def iter_assist_requests():
            config = embedded_assistant_pb2.AssistConfig(
                audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                    encoding='LINEAR16',
                    sample_rate_hertz=16000,
                    volume_percentage=0,
                ),
                dialog_state_in=embedded_assistant_pb2.DialogStateIn(
                    language_code=self.language_code,
                    conversation_state=self.conversation_state,
                    is_new_conversation=self.is_new_conversation,
                ),
                device_config=embedded_assistant_pb2.DeviceConfig(
                    device_id=self.device_id,
                    device_model_id=self.device_model_id,
                ),
                text_query=text_query,
            )
            # Continue current conversation with later requests.
            self.is_new_conversation = False
            req = embedded_assistant_pb2.AssistRequest(config=config)
            assistant_helpers.log_assist_request_without_audio(req)
            yield req

        text_response = None
        html_response = None
        for resp in self.assistant.Assist(iter_assist_requests(),
                                          self.deadline):
            assistant_helpers.log_assist_response_without_audio(resp)
            if resp.screen_out.data:
                html_response = resp.screen_out.data
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                self.conversation_state = conversation_state
            if resp.dialog_state_out.supplemental_display_text:
                text_response = resp.dialog_state_out.supplemental_display_text
        return text_response, html_response


@click.command()
@click.option('--api-endpoint', default=ASSISTANT_API_ENDPOINT,
              metavar='<api endpoint>', show_default=True,
              help='Address of Google Assistant API service.')
@click.option('--credentials',
              metavar='<credentials>', show_default=True,
              default=os.path.join(click.get_app_dir('google-oauthlib-tool'),
                                   'credentials.json'),
              help='Path to read OAuth2 credentials.')
@click.option('--device-model-id',
              metavar='<device model id>',
              required=True,
              help=(('Unique device model identifier, '
                     'if not specifed, it is read from --device-config')))
@click.option('--device-id',
              metavar='<device id>',
              required=True,
              help=(('Unique registered device instance identifier, '
                     'if not specified, it is read from --device-config, '
                     'if no device_config found: a new device is registered '
                     'using a unique id and a new device config is saved')))
@click.option('--lang', show_default=True,
              metavar='<language code>',
              default='en-US',
              help='Language code of the Assistant')
@click.option('--display', is_flag=True, default=True,
              help='Enable visual display of Assistant responses in HTML.')
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='Verbose logging.')
@click.option('--grpc-deadline', default=DEFAULT_GRPC_DEADLINE,
              metavar='<grpc deadline>', show_default=True,
              help='gRPC deadline in seconds')

def main(api_endpoint, credentials,
         device_model_id, device_id, lang, display, verbose,
         grpc_deadline, *args, **kwargs):
    # Setup logging.
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    # Load OAuth 2.0 credentials.
    try:
        with open(credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
    except Exception as e:
        logging.error('Error loading credentials: %s', e)
        logging.error('Run google-oauthlib-tool to initialize '
                      'new OAuth 2.0 credentials.')
        return

    # Create an authorized gRPC channel.
    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, api_endpoint)
    logging.info('Connecting to %s', api_endpoint)

    def hasNumbers(inputString):
        return any(char.isdigit() for char in inputString)

    with SampleTextAssistant(lang, device_model_id, device_id, display,
                             grpc_channel, grpc_deadline) as assistant:
        import time
        while True:
            '''query = click.prompt('')
            click.echo('<you> %s' % query)
            response_text, response_html = assistant.assist(text_query=query)
            if display and response_html:
                system_browser = browser_helpers.system_browser
                system_browser.display(response_html)
            if response_text:
                click.echo('<@assistant> %s' % response_text)'''

            '''query = click.prompt('')
            click.echo('<you> %s' % query)
            waste, response_html = assistant.assist1(text_query=query)
            response_text, waste = assistant.assist2(text_query=query)
            if display and response_html:
                system_browser = browser_helpers.system_browser
                system_browser.display(response_html)
            if response_text:
                click.echo('<@assistant> %s' % response_text)'''

            temp=''
            query=''
            response_text=''
            try:
                with open(ASSISTANTFOLDER+'query.txt', 'r') as f:
                    temp=f.read()

                temp2=temp

                if temp2!='':
                    query=temp.replace('\n', ' ')

                if query!='':
                    try:
                        os.remove(ASSISTANTFOLDER+'query.txt')
                    except:
                        pass
                    click.echo('<you> %s' % query)
                    waste, response_html = assistant.assist1(text_query=query)
                    response_text, waste = assistant.assist2(text_query=query)

                    if response_text!=None and response_html!=None:
                        from bs4 import BeautifulSoup

                        resp=''

                        #if query.count('weather')>0 or hasNumbers(response_text):
                        if query.count('game')==0 and query.count('quiz')==0:
                            print(temp)
                            resp+=response_text

                        htmlcode=response_html

                        soup = BeautifulSoup(htmlcode,features="html.parser")
            
                        x=soup.findAll('div' , class_ = 'show_text_content')
                        
                        if(len(x)==0):
                            x=soup.findAll('div' , class_ = 'G6dPLb MUxGbd v0nnCb H7ORec aLF0Z')
                        
                        if(len(x)==0):
                            x=soup.findAll('div' , class_ = 'BmP5tf')

                        y=soup.findAll('button', class_ = 'suggestion follow-up-query')

                        if len(y)==0:
                            y=soup.findAll('div', class_ = 'assistant-bar-content')

                        s=t=''

                        for i in x:
                            try:
                                s+=(i.get_text())+'\n'
                            except:
                                pass
                        
                        for i in y:
                            try:
                                t+=(i.get_text())+'\n'
                            except:
                                pass

                        if t!='\n' and len(t)>2:
                            resp+='\n Response from the web: \n'+s+'\nTry Saying: \n'+t
                        else:
                            resp+='\n Response from the web: \n'+s

                        with open(ASSISTANTFOLDER+'response.txt', 'w+', encoding='utf-8') as h:
                            h.write(resp)

                    elif response_text!=None:

                        resp=response_text

                        if(response_html!=None):
                            from bs4 import BeautifulSoup

                            htmlcode=response_html

                            soup = BeautifulSoup(htmlcode,features="html.parser")
                
                            x=soup.findAll('div' , class_ = 'show_text_content')
                            
                            if(len(x)==0):
                                x=soup.findAll('div' , class_ = 'G6dPLb MUxGbd v0nnCb H7ORec aLF0Z')
                            
                            if(len(x)==0):
                                x=soup.findAll('div' , class_ = 'BmP5tf')

                            y=soup.findAll('button', class_ = 'suggestion follow-up-query')

                            if len(y)==0:
                                y=soup.findAll('div', class_ = 'assistant-bar-content')

                            s=t=''

                            for i in x:
                                try:
                                    s+=(i.get_text())+'\n'
                                except:
                                    pass
                            
                            for i in y:
                                try:
                                    t+=(i.get_text())+'\n'
                                except:
                                    pass

                            if t!='\n' and len(t)>2:
                                resp='\n Response from the web: \n'+s+'\nTry Saying: \n'+t
                            else:
                                resp='\n Response from the web: \n'+s

                        with open(ASSISTANTFOLDER+'response.txt', 'w+', encoding='utf-8') as h:
                            h.write(resp)

                    elif response_html!=None:

                        #system_browser = browser_helpers.system_browser
                        #system_browser.display(response_html)

                        from bs4 import BeautifulSoup

                        htmlcode=response_html

                        soup = BeautifulSoup(htmlcode,features="html.parser")
            
                        x=soup.findAll('div' , class_ = 'show_text_content')
                        
                        if(len(x)==0):
                            x=soup.findAll('div' , class_ = 'G6dPLb MUxGbd v0nnCb H7ORec aLF0Z')
                        
                        if(len(x)==0):
                                x=soup.findAll('div' , class_ = 'BmP5tf')

                        y=soup.findAll('button', class_ = 'suggestion follow-up-query')

                        if len(y)==0:
                            y=soup.findAll('div', class_ = 'assistant-bar-content')

                        s=t=''

                        for i in x:
                            try:
                                s+=(i.get_text())+'\n'
                            except:
                                pass
                        
                        for i in y:
                            try:
                                t+=(i.get_text())+'\n'
                            except:
                                pass
                        
                        if t!='\n' and len(t)>2:
                            resp='\n Response from the web: \n'+s+'\nTry Saying: \n'+t
                        else:
                            resp='\n Response from the web: \n'+s

                        with open(ASSISTANTFOLDER+'response.txt', 'w', encoding='utf-8') as f:
                            f.write(resp)
                    else:
                        with open(ASSISTANTFOLDER+'response.txt', 'w', encoding='utf-8') as f:
                            f.write('Could not respond to that')

                    if display and response_html:
                        #system_browser = browser_helpers.system_browser
                        #system_browser.display(response_html)
                        pass
                    if response_text:
                        click.echo('<@assistant> %s' % response_text)

            except:
                pass
            time.sleep(1)


if __name__ == '__main__':
    main()
