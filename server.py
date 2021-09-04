import asyncio

class ClientServerProtocol(asyncio.Protocol):
    storage = {}
    error_string = 'error\nwrong command\n\n'

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())
    
    def process_data(self, data):
        try:
            command, message = data.split(' ', 1)
            length_message = len(message.split(' '))
            if (command == 'put') and (length_message == 3):
                res = self._put(message)
            elif (command == 'get') and (length_message == 1):
                res = self._get(message)
            else:
                res = self.error_string
        except ValueError:
            res = self.error_string
        return res

    def _put(self, message):
        try:
            # Here I delete the \n from the end of message using [:-1]
            message_splt = message[:-1].split(' ')
            key = message_splt[0]
            value = float(message_splt[1])
            timestamp = int(message_splt[2])
            store = self.storage
            if key in store and not(timestamp in store[key][:][0]):
                # If metrics with same key and timestamp exists we overwrite
                # it with new value according to protocol.Otherwise append 
                store[key].append((timestamp,value))
            else:
                store[key] = [(timestamp, value)]
        except (ValueError, IndexError):
            return self.error_string
        return ('ok\n\n')

    def _get(self, message):
        try:
            key = message[:-1]
            #print("message is ", key, ' .')
            #print('store is ', self.storage)
            if key == '*':
                res = self._stringify_dict(self.storage)
            elif key in self.storage:
                res = self._stringify_dict({key : self.storage[key]})
            elif key in (' ', ''):
                res = self.error_string
            else:
                res = self._stringify_dict({})    
            return res
        except (ValueError, IndexError):
            return self.error_string

    @staticmethod
    def _stringify_dict(storage):
        # This method is putting dictionary into the string,that we send client
        string = 'ok\n'
        for key in storage:
            # We cycle through the keys and through entries in that key's tuple
            for entry in storage[key]:
                string += '{} {} {}\n'.format(key,
                        str(entry[1]),
                        str(entry[0]))
        return(string + '\n')

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
