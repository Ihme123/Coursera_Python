import socket
import time

class ClientError(Exception):
    pass

class Client:
    def __init__(self, host, port, timeout=None):
        sock = socket.create_connection((host,port), timeout)
        self.sock = sock
        if timeout:
            sock.settimeout(timeout)
            
    def parse_dict(recieved_data):
        data = recieved_data.decode('utf-8')
        res = {}
        if data[:2] != 'ok':
            raise ClientError
        # if key is non-existing, server will return empty dict:
        elif data == 'ok\n\n':
            return res
        else:
            # data[3:-3] is removing \n from beginning and end
            try: 
                data = data[3:-2].split('\n')
                for string in data:
                    splt = string.split(' ')
                    # Here I use setdefault to create dict key if it doesn't exist
                    res.setdefault(splt[0], []).append(
                            (int(splt[2]), float(splt[1])))
                # Sort the tuples by the timestamp
                for key in res:
                    res[key].sort(key=lambda s:s[0])
            except (IndexError, ValueError):
                raise ClientError
        return res
    
    # I wrote this func not to overload put function
    def string_format(key, value, timestamp):
        return ('put ' + str(key) + ' ' + str(value) + ' ' 
                + str(timestamp) + '\n').encode('utf8')
    
    def get(self, key):
        '''
        Key parameter is the name of the metrics we want to collect from server. We can use 
        '*' to recieve all the metrics
        We recieve the string from server and put the values and timestamps into a dict with
        format like this {'key': [(timestamp1, value1), (timestamp2, value2)]}
        '''
        self.sock.sendall(('get ' + str(key) + '\n').encode('utf8'))
        data = self.sock.recv(1024)
        
        return Client.parse_dict(data)
    
    def put(self, key, value, timestamp=None):
        '''
        Key is the name of the metrics we put - ex. 'palm.cpu' or 'eardrum.memory'
        Value is the number we want to assign to this key - ex. 0.5
        Timestamp is the time we want to assign to given metrics. ex. 1150864251
        
        Example of usage:
        client.put('eardrum.cpu', 4, timestamp=1150864248)
        '''
        try:
            if not timestamp:
                timestamp = int(time.time())
            self.sock.sendall(Client.string_format(key, value, timestamp))
            
            data = self.sock.recv(1024)
            if data.decode('utf-8)')[:2] != 'ok':
                raise ClientError
        except socket.timeout:
            print('Send Data Timeout')
        except socket.error as er:
            print("Send Data Error {}".format(er))

    
