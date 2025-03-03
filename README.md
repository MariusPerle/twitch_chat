# twitch_chat
a simple way to connect, send and receive messanges from Twitch chat

## Requirements
Python 3.6 +

## Usage
1. install library
    ```bash
    pip install git+https://github.com/MariusPerle/twitch_chat
    ```
1. import class
    ```python
    from twitch_chat import TwitchChat
    ```
1. connect to chat with Token from https://twitchapps.com/tmi/
    ```python
    my_chat = TwitchChat(oath='do not share', bot_name='your_bot', channel_name='channel_I_want_to_join')
    ```
1. send or receive message
    ```python
   while True: 
       user, message = my_chat.listen_to_chat()   
       # do something
       my_chat.send_to_chat('hi')  
   ```
