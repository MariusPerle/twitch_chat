from socket import socket


class TwitchChat:

    def __init__(self, chat_socket: socket, channel: str):
        self.socket = chat_socket
        self.channel = channel

    def send_to_chat(self, message: str):
        """
        sends a message to twitch chat

        :param message: message to send in twitch chat
        :return:
        """

        message_temp = f'PRIVMSG #{self.channel} :{message}'
        self.socket.send(f'{message_temp}\n'.encode())

    def listen_to_chat(self) -> (str, str):
        """
        listens to chat and calls function if message is received
        designed for endless loops with ping pong socket concept

        :return: user, message from chat or None
        """
        read_buffer = self.socket.recv(1024).decode()

        for line in read_buffer.split('\r\n'):
            # ping pong to stay alive
            if 'PING' in line and 'PRIVMSG' not in line:
                self.socket.send('PONG tmi.twitch.tv\r\n'.encode())

            # reacts at user message
            elif line != '':
                parts = line.split(':', 2)
                return parts[1].split('!', 1)[0], parts[2]


def join_chat(oath: str, bot_name: str, channel_name: str, server: str = 'irc.twitch.tv',
              port: int = 6667) -> TwitchChat:
    """
    joins a chat and returns TwitchChat

    :param oath: oath token from bot
    :param bot_name: name from bot
    :param channel_name: broadcaster name
    :param server: IP address of api
    :param port: port of api
    :return: TwitchChat object for further uses
    """
    irc = socket()
    irc.connect((server, port))
    irc.send(f'PASS oauth:{oath}\nNICK {bot_name}\n Join #{channel_name}\n'.encode())

    loading = True
    while loading:
        read_buffer_join = irc.recv(1024)
        read_buffer_join = read_buffer_join.decode()

        for line in read_buffer_join.split('\n')[0:-1]:
            # checks if loading is complete
            loading = 'End of /NAMES list' not in line

    return TwitchChat(chat_socket=irc, channel=channel_name)
