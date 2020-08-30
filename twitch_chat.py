from socket import socket


class TwitchChat:

    def __init__(self, channel_name: str, oath: str = None, bot_name: str = None):
        # these may change in the future
        server = 'irc.twitch.tv'
        port = 6667

        self.socket = socket()
        self.channel = channel_name
        self.socket.connect((server, port))

        self.allowed_to_post = oath and bot_name

        if self.allowed_to_post:
            self.socket.send(f'PASS oauth:{oath}\nNICK {bot_name}\n Join #{channel_name}\n'.encode())
        else:
            self.socket.send(f"NICK justinfan0\n".encode('utf-8'))
            self.socket.send(f"JOIN #{channel_name}\n".encode('utf-8'))

        loading = True
        while loading:
            read_buffer_join = self.socket.recv(1024)
            read_buffer_join = read_buffer_join.decode()

            for line in read_buffer_join.split('\n')[0:-1]:
                # checks if loading is complete
                loading = 'End of /NAMES list' not in line

    def send_to_chat(self, message: str):
        """
        sends a message to twitch chat if it's possible

        :param message: message to send in twitch chat
        :return:
        """

        if self.allowed_to_post:
            message_temp = f'PRIVMSG #{self.channel} :{message}'
            self.socket.send(f'{message_temp}\n'.encode())
        else:
            raise RuntimeError('Bot has no permission to sent messages get oath token at http://twitchapps.com/tmi/')

    def listen_to_chat(self) -> (str, str):
        """
        listens to chat and returns name and
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
