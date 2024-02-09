
## This file contains the definition of the Py-Waku module
## that is going to be delivered when the module is installed.

import ctypes
from cffi import FFI

# Create an FFI object
ffi = FFI()

# Load the C library
libwaku = ffi.dlopen('lib/libwaku.so')

# Declare the C functions
ffi.cdef("""
typedef void (*WakuCallBack) (int callerRet, const char* msg, size_t len);

// Creates a new instance of the waku node.
// Sets up the waku node from the given configuration.
// Returns a pointer to the Context needed by the rest of the API functions.
void* waku_new(
             const char* configJson,
             WakuCallBack callback,
             void* userData);

int waku_start(void* ctx,
               WakuCallBack callback,
               void* userData);

int waku_stop(void* ctx,
              WakuCallBack callback,
              void* userData);

int waku_version(void* ctx,
                 WakuCallBack callback,
                 void* userData);

void waku_set_event_callback(WakuCallBack callback);

int waku_content_topic(void* ctx,
                       const char* appName,
                       unsigned int appVersion,
                       const char* contentTopicName,
                       const char* encoding,
                       WakuCallBack callback,
                       void* userData);

int waku_pubsub_topic(void* ctx,
                      const char* topicName,
                      WakuCallBack callback,
                      void* userData);

int waku_default_pubsub_topic(void* ctx,
                              WakuCallBack callback,
                              void* userData);

int waku_relay_publish(void* ctx,
                       const char* pubSubTopic,
                       const char* jsonWakuMessage,
                       unsigned int timeoutMs,
                       WakuCallBack callback,
                       void* userData);

int waku_relay_subscribe(void* ctx,
                         const char* pubSubTopic,
                         WakuCallBack callback,
                         void* userData);

int waku_relay_unsubscribe(void* ctx,
                           const char* pubSubTopic,
                           WakuCallBack callback,
                           void* userData);

int waku_connect(void* ctx,
                 const char* peerMultiAddr,
                 unsigned int timeoutMs,
                 WakuCallBack callback,
                 void* userData);
""")

##################################################################
## helpers

def process_callback(ret, char_p, len, callback):
  ## Converts the data from C space (char* + len) into Python string
  ## and then, calls the Python callback which should only have two parameters:
  ## First param - integer. 0 means OK. Otherwise, means error, with error code (see libwaku.h)
  ## Second param - string. Gives detail of the feedback returned by the libwaku

  byte_string = ffi.buffer(char_p, len)[:]  # Use ffi.buffer to access memory directly
  callback(ret, byte_string)

##################################################################

# Define the callback function type within the module
CallbackType = ffi.callback("void(int, char*, size_t)")

# Python wrapper functions
def waku_new(config_json, callback):
  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_new(config_json,
                          CallbackType(cb), # Convert the Python callback to a C callback
                          ffi.cast("void*", 0))

def waku_start(ctx, callback):
  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_start(ctx,
                            CallbackType(cb),
                            ffi.cast("void*", 0))

def waku_stop(ctx, callback):
  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_stop(ctx,
                           CallbackType(cb),
                           ffi.cast("void*", 0))

def waku_version(ctx, callback):
  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_version(ctx,
                              CallbackType(cb),
                              ffi.cast("void*", 0))

my_python_callback = None

@ffi.callback("void(int, char*, size_t)")
def handle_event(ret, char_p, len):
  ## Handle the event from the C layer
  process_callback(ret, char_p, len, my_python_callback)

def waku_set_event_callback(callback):
  global my_python_callback
  my_python_callback = callback

  libwaku.waku_set_event_callback(handle_event)

def waku_content_topic(ctx,
                       appName,
                       appVersion,
                       contentTopicName,
                       encoding,
                       callback):

  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_content_topic(ctx,
                                    appName,
                                    appVersion,
                                    contentTopicName,
                                    encoding,
                                    CallbackType(cb),
                                    ffi.cast("void*", 0))

def waku_pubsub_topic(ctx, topicName, callback):

  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_pubsub_topic(ctx,
                                   topicName,
                                   CallbackType(cb),
                                   ffi.cast("void*", 0))

def waku_default_pubsub_topic(ctx, callback):

  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_default_pubsub_topic(ctx,
                                           CallbackType(cb),
                                           ffi.cast("void*", 0))

def waku_relay_publish(ctx,
                       pubSubTopic,
                       jsonWakuMessage,
                       timeoutMs,
                       callback):

  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_relay_publish(ctx,
                                    pubSubTopic,
                                    jsonWakuMessage,
                                    timeoutMs,
                                    CallbackType(cb),
                                    ffi.cast("void*", 0))

def waku_relay_subscribe(ctx,
                         pubSubTopic,
                         callback):

  @ffi.callback("void(int, char*, size_t)")
  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_relay_subscribe(
                                ctx,
                                pubSubTopic,
                                cb,
                                ffi.cast("void*", 0))

def waku_relay_unsubscribe(ctx,
                           pubSubTopic,
                           callback):

  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_relay_unsubscribe(
                                ctx,
                                pubSubTopic,
                                CallbackType(cb),
                                ffi.cast("void*", 0))

def waku_connect(ctx,
                 peerMultiAddr,
                 timeoutMs,
                 callback):

  def cb(ret, char_p, len):
    process_callback(ret, char_p, len, callback)

  return libwaku.waku_connect(
                            ctx,
                            peerMultiAddr,
                            timeoutMs,
                            CallbackType(cb),
                            ffi.cast("void*", 0))

