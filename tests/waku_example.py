from flask import Flask
import argparse
import waku

def handle_event(ret, msg):
  if ret == 0: ## RET_OK
    print("Ok event received: %s" % msg)
  else:
    print("Error: %s" % msg)

def call_waku(func):
  ret = func()
  if (ret != 0):
    print("Error in %s. Error code: %d" % (locals().keys(), ret))
    exit(1)

# Parse params
parser = argparse.ArgumentParser(description='libwaku integration in Python.')
parser.add_argument('-d', '--host', dest='host', default='0.0.0.0',
                    help='Address this node will listen to. [=0.0.0.0]')
parser.add_argument('-p', '--port', dest='port', default=60000, required=True,
                    help='Port this node will listen to. [=60000]')
parser.add_argument('-k', '--key', dest='key', default="", required=True,
                    help="""P2P node private key as 64 char hex string.
e.g.: 364d111d729a6eb6d2e6113e163f017b5ef03a6f94c9b5b7bb1bb36fa5cb07a9""")
parser.add_argument('-r', '--relay', dest='relay', default="true",
                    help="Enable relay protocol: true|false [=true]")
parser.add_argument('--peer', dest='peer', default="",
                    help="Multiqualified libp2p address")

args = parser.parse_args()

# The next 'json_config' is the item passed to the 'waku_new'.
json_config = "{ \
                \"host\": \"%s\",   \
                \"port\": %d,       \
                \"key\": \"%s\",    \
                \"relay\": %s      \
            }" % (args.host,
                  int(args.port),
                  args.key,
                  "true" if args.relay else "false")

print("Starting node with config: %s" % json_config)

ctx = waku.waku_new(json_config.encode('ascii'),
                    lambda ret, msg:
                      print("Error creating new waku node: %s" %
                            msg))

# Retrieve the current version of the library
waku.waku_version(ctx,
                  lambda ret, msg:
                    # print("Git Version")
                    # print("Git Version: %s" %
                    #       ctypes.c_char_p(ctypes.addressof(msg)).value.decode('utf-8')))
                    print("Git Version: %s" % msg))

# Retrieve the default pubsub topic
default_pubsub_topic = ""
waku.waku_default_pubsub_topic(
    ctx,
    lambda ret, msg: (
        globals().update(default_pubsub_topic = msg),
        print("Default pubsub topic: %s" % msg)))

print("Bind addr: {}:{}".format(args.host, args.port))
print("Waku Relay enabled: {}".format(args.relay))

# Set the event callback
callback = handle_event # This line is important so that the callback is not gc'ed
waku.waku_set_event_callback(callback)

# Start the node
waku.waku_start(ctx,
                lambda ret, msg:
                  print("Error starting: %s" % msg))

waku.waku_connect(ctx,
                  args.peer.encode('utf-8'),
                  10000,
                  # onErrCb
                  lambda ret, msg:
                    print("Error calling waku_connect: %s" % msg))

waku.waku_relay_subscribe(ctx,
                          default_pubsub_topic.encode('utf-8'),
                          callback)

# Simply avoid the app to end. We could have a UI in this point or a flask server
# that could attend user actions.
a = input()

