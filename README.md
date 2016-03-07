

# Starting the SDK

The SDK is started by calling ```exp.start``` and specifying your credentials and configuration options as keyword arguments. ```exp.start``` will start additional threads to process network events. You may supply user, device, or consumer app credentials. You can also authenticate in pairing mode.

When ```exp.start``` returns, you are authenticated and can begin using the SDK. 



## User Credentials

Users must specify their ```username```, ```password```, and ```organization``` as keyword arguments to ```exp.start```.

```python
import exp

exp.start(username='joe@joemail.com', password='JoeRocks42', organization='joesorg')

```

## Device Credentials

Devices must specify their ```uuid``` and ```secret``` as keyword arguments.

```python
import exp

exp.start(uuid='[uuid]', secret='[secret]')

```

## Consumer App Credentials

Consumer apps must specify their ```uuid``` and ```api_key``` as keyword arguments.

```python
import exp

exp.start(uuid='[uuid]', api_key='[api key]')

```

## Pairing Mode

Advanced users can authenticate in pairing mode by setting ```allow_pairing``` to ```False```.

```python
import exp

exp.start(allow_pairing=False)

```


## Additional Options

Name | Default | Description
--- | --- | ---
host | ```'https://api.goexp.io'``` | The api server to authenticate with.
enable_network | ```True``` | Whether to enable real time network communication. If set to ```False``` you will be unable to listen on the [EXP network](# Communicating on the EXP Network).

### Exceptions

If the arguments specified to ```exp.start``` are invalid or incomplete an ```exp.RuntimeError``` will be raised.





# Communicating on the EXP Network

The EXP network facilitates real time communication between entities connected to EXP. A user or device can broadcast a JSON serializable payload to users and devices in your organization, and listeners to those broadcasts can respond to the broadcasters.

### Channels

All messages on the EXP network are sent over a channel. Channels have a name, and two flags: ```system``` and ```consumer```.

```python
channel = exp.get_channel('my_channel', system=False, consumer=False)
```

Use ```system=True``` to get a system channel. You cannot send messages on a system channels but can listen for system notifications, such as updates to API resources.

Use ```consumer=True``` to get a consumer channel. Consumer devices can only listen or broadcast on consumer channels. When ```consumer=False``` you will not receive consumer device broadcasts and consumer devices will not be able to hear your broadcasts.

Both ```system``` and ```consumer``` default to ```False```. Consumer devices will be unable to broadcast or listen to messages on non-consumer channels.


### Broadcasting

Use the broadcast method of a channel object to send a named message containing an optional JSON serializable payload to other entities on the EXP network. You can optionally include a timeout to wait for responses to the broadcast. The broadcast will block for approximately the given timeout and return a ```list``` of response payloads. Each response payload can any JSON serializable type.

```python

channel = exp.get_channel('my_channel')
responses = channel.broadcast(name='my_event', timeout=5, payload='hello')
[print response for response in responses]

```


### Listening

To listen for broadcasts, call the listen method of a channel object and pass in the name of the event you wish to listen for. When EXP listener has been registered and can start receiving events, a ```listener``` object will be returned. 

Call the ```wait``` method of a listener to block until a broadcast is received, passing in a timeout in seconds. If ```timeout``` elaspes and no broadcasts have been received, ```wait``` will return ```None```.

Once a listener is created, it will receive broadcasts in a background thread even when not waiting. Calling ```wait``` will first attempt to return the oldest broadcast in the queue. Queued broadcasts will be discarded after ~60s if not retrieved during a ```wait```.

```python

channel = exp.get_channel('my_channel')
listener = channel.listen('my_event')

while True:
  broadcast = listener.wait(5)
  if broadcast:
    print 'Message received!'
    print broadcast.payload
    listener.cancel()
    break

```


### Responding

To respond to broadcast, call the respond method on the broadcast object, optionally passing in a JSON serializable response payload.

```python

channel = exp.get_channel('my_channel')
listener = channel.listen(name='my_event')

while True:
  broadcast = listener.wait(5)
  if broadcast and broadcast.payload is 'hello':
    print 'Responding to broadcast.'
    broadcast.respond('Nice to meet you!')

```

# SDK Reference


## Startup
```exp.start(username=None, password=None, uuid=None, secret=None, api_key=None, enable_network=True, host='https://api.goexp.io', allow_pairing=False)```: Start the SDK with the given set of options. See [Starting the SDK](#starting-the-sdk).

## Exceptions

- ```exp.ExpError```: Base class for errors raised by the SDK.
- ```exp.AuthenticationError```: Raised when SDK cannot authenticate.
- ```exp.RuntimeError```: Raised when options pass to ```exp.start``` are invalid or inconsistent. 
- ```exp.HttpError```: Raised when an API request encouters and error. This exception has the following attributes:
  - ```code```: The API REST code of the error.
  - ```status```: The HTTP status code received.
  - ```message```: A human readable description of the encountered error.
- ```exp.UnexpectedError```: Raised when an SDK method encounters an unexpected exception.

## Devices

- ```device = exp.get_device(uuid)```: Get a device by uuid.
- ```device = exp.create_device(document)```: Create (and save) a device given a device document, a dictionary.
- ```devices = exp.find_devices(params)```: Get a list of devices given a dictionary of query parameters. See the API docs.
- ```device.uuid```: The device's uuid.
- ```device.document```: The underlying device's document, a dictionary.
- ```device.get_channel(system=False, consumer=False)```: Get a [channel](#Channels) for communication about this device. 

## Things
- ```thing = exp.get_thing(uuid)```: Get a thing by uuid.
- ```thing = exp.create_thing(document)```: Create (and save) a thing given a thing document, a dictionary.
- ```thing = exp.find_things(params)```: Get a list of things given a dictionary of query parameters. See the API docs.
- ```thing.uuid```: The thing's uuid.
- ```thing.document```: The underlying thing's document, a dictionary.
- ```thing.get_channel(system=False, consumer=False)```: Get a [channel](#Channels) for communication about this thing. 

# Experiences
- ```experience = exp.get_experience(uuid)```: Get an experience by uuid.
- ```experience = exp.create_experience(document)```: Create and save  new experience from document.
- ```experiences = exp.find_experiences(params)```: Get a list of experiences given a dictionary of query params. See the API docs.
- ```experience.uuid```: The experience's uuid.
- ```experience.document```: The underlying experience's document, a dictionary.
- ```experience.get_channel(system=False, consumer=False)```: Get a [channel](#Channels) for communication about this experience.
- 
# Locations
- ```location = exp.get_location(uuid)```: Get a location by uuid.
- ```location = exp.create_location(document)```: Create and save  new experience from document.
- ```locations = exp.find_locations(params)```: Get a list of locations given a dictionary of query params. See the API docs.
- ```location.uuid```: The locations's uuid.
- ```location.document```: The underlying experience document, a dictionary.
- ```location.get_channel(system=False, consumer=False)```: Get a [channel](#Channels) for communication about this location.
- ```location.get_zones()```: Get a list of [zones](#Zones) that are part of this location.


# Zones
- ```zone.document```: The underlying zone's document, a dictionary.
- ```zone.get_channel(system=False, consumer=False)```: Get a [channel](#Channel) for communication about this zone.

# Content

# Feeds

# Channel
- ```channel = exp.get_channel(name, system=False, consumer=False)```: Get a channel by name.
- ```responses = channel.broadcast(name, payload=None, timeout=0):``` Send a broadcast on this channel, with name ```name``` and JSON serializable payload ```payload```. Wait for ```timeout``` seconds for responses. ```responses``` will be a list of JSON serializable objects, one item per response is order the response was received.
- ```listener = channel.listen(name)```: Listen for messages with name ```name``` on the given channel. Returns a [Listener](#listener) after the listener has been registered internally and can receive events.



##Listener
- ```listener.cancel()```: Permanently detach the listener. Cannot be undone.
- ```broadcast = listener.wait(timeout=0)```: Block for broadcasts for ```timeout``` seconds.  Any broadcasts received by the listener when not waiting are queued. If there is a broadcast in the queue, the oldest broadcast will be consumed and returned immediately when ```wait``` is called. If no broadcasts are queued and none are received in ```timeout``` seconds, ```wait``` returns ```None```.

# Broadcast
- ```broadcast.payload```: The payload of the broadcast. Always JSON serializable type.
- ```broadcast.respond(payload)```: Respond to the broadcast. ```payload``` is a JSON serializable response to send back to the broadcaster.







