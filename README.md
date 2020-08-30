# twitch_chat
a simple way to connect, send and receive messanges from Twitch chat

## Requirements
Python 3.7 +

## Usage
1. download twitch_chat.py
1. import script
    ```python
    from twitch_chat import join_chat
    ```
1. connect to chat
    ```python
    my_chat = TwitchChat(oath='do not share', bot_name='test', channel_name='0815_truppe')
    my_chat_listen_only = TwitchChat(channel_name='0815_truppe')
    ```
1. send or receive message
    ```python
   while True: 
       user, message = my_chat.listen_to_chat()   
       # do something
       my_chat.send_to_chat('hi')  # raises Error with my_chat_listen_only  
   ```
