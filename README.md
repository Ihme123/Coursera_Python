# PythonServerAsync


My asynchronic Server + Client solution.

## Protocol: 

The protocol supports two types of requests to the server from the client side:
- sending data to save it on the server (put command)
- getting saved data (get command)

## Format:

- put : **client.put("my_metrics", Value, Timestamp)**
- get : **client.get("my_metrics")**

## Details:

- put can be called without timestamp (for example, **client.put("server1.cpu", 15.0)**), then timestamp should automatically be equal to current time — int(time.time()).
- get can be called with * metric, it means "give me all the data saved" (for example, **client.get("*")**)

## Response from server:
- to put command: 
    if succesfully put into memory **ok\n**
    if something went wrong **error\nwrong command\n\n**
 -to get command:
    if succesfully got something from memory **[(timestamp1, value1), (timestamp2,value2), ...]**
    if we got nothing from memory or if given key doesn't exist **ok\n\n**
    if there was an error **error\nwrong command\n\n**
    
 ## Examples:
 from client import Client
 
 client = Client("127.0.0.1", 8888, timeout=10)
 
 client.put("server1.disk_usage", 66.0, timestamp= 1150864940)
 
 >ok
 
 client.put("server2.cpu_usage", 32.6, timestamp= 1150864941)
 
 >ok
 
client.get("*")

>ok

>server1.disk_usage 66.0 1150864940


>server2.cpu_usage 32.6 1150864941


client.get("server1.disk_usage")


>ok


>server1.disk_usage 66.0 1150864940


Was made during MIPT&amp;Mail.ru python course (https://www.coursera.org/learn/diving-in-python/)
Week 5 and 6 exercises.
