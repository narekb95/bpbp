## Parameters



## Testing

Run two nodes on two different ports:

- Inbound:

```
    python3 src/node.py params/bitcoin.json
```
- Outbound:
```
    python3 src/node.py params/bitcoin.json  --port=3322 --outbound_ips=0.0.0.0:8333
```
