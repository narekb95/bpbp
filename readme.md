## Parametsr:

- Default parameters can be read as options in a json file.
- Optionally, one can override parameters using commandline options.
- This can be done with syntex: `--[param]=[value]`.

| CMD Parameter  | JSON Option | Description |
| ------------- | ------------- | ------------- |
| host  | DEFAULT_PORT | [Is this needed?] |
| port  | DEFAULT_HOST | Port to listen to |
| max_inbound  | MAX_INBOUND | Content Cell  |
| outbound-ips  | [see outbound section]  | Content Cell  |

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
