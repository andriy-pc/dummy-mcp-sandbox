# Dummy JSON RPC practice
Run the following commands to test local JSON PRC:
```
echo '{"jsonrpc": "2.0", "id": 1, "method": "add", "params": [3, 5]}' | python dummy_json_rpc.py
echo '{"jsonrpc": "2.0", "id": 2, "method": "greet", "params": ["Alice"]}' | python dummy_json_rpc.py
```