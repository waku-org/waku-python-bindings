## Helper script that allows to start the `waku_example.py`
## and pass it some typical arguments that made the node to connect to a peer.

## Notice that the other peer is expected to a native nwaku running with the following
## configuration file:
## ports-shift = 0

## pubsub-topic = [ "/waku/2/default-waku/proto" "/waku/2/testing-store" ]
## staticnode = [ "/ip4/0.0.0.0/tcp/60001/p2p/16Uiu2HAm2eqzqp6xn32fzgGi8K4BuF88W4Xy6yxsmDcW8h1gj6ie" ]
## log-level = "DEBUG"
## nodekey = "0d714a1fada214dead6dc9c7274585eca0ff292451866e7d6d677dc818e8ccd2"
## lightpush = true
## store = true
## store-message-db-url = "sqlite://sqlite_folder/store.sqlite3"
## store-message-retention-policy = "capacity:100000000"
## rpc-admin=true
## rest-admin=true
## rest = true
## metrics-server = true
## discv5-discovery = true
## discv5-enr-auto-update = true

./venv/bin/python3 \
        tests/waku_example.py \
          -p 60001 \
          -k 364d111d729a6eb6d2e6113e163f017b5ef03a6f94c9b5b7bb1bb36fa5cb07a9 \
          -r 1 \
          --peer /ip4/127.0.0.1/tcp/60000/p2p/16Uiu2HAmVFXtAfSj4EiR7mL2KvL4EE2wztuQgUSBoj2Jx2KeXFLN
