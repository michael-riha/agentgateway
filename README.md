
> [!WARNING]  
> This is a very rudimentary project and setup. 
> It is not working as expected yet!
> - `agentgateway` does not yet route to MCP `everything` contianer, yet!

> [!CAUTION]
> Only view this as a WORK IN PROGRESS and educational exercise. 

# `agentgateway` Docker compose setup

this project (`compose.yaml`) includes:
  - `agentgateway`
    - for general purpose to gain knowhow
      - ✅ got it working with AWS Bedrock
      - TODOs:
        - learn more how to use MCPs
        - route `echo` plain HTTP as gateway
        - try an openAPI server 
        - ... find time⏳️
  - `tzolov/mcp-everything-server:v2` 
    - for testing with an external MCP **❌ NOT WORKING**
  - `ghcr.io/modelcontextprotocol/inspector`
    - for inspecting and debugging MCP interactions ✅
  - `echo`
    - for debugging and output of HTTP interaction via the gateway



---

# `aws` `bedrock` for `LLM`-routing

- [add config](https://github.com/michael-riha/agentgateway/blob/69b8b6e9c30d1f29594d686382dd63a834bb61be/services_configs/agentgateway/config%20copy.yaml#L21-L33)
- [for the `aws`-credentials:
  - [either via ENV-vars (preferred)](https://github.com/michael-riha/agentgateway/blob/69b8b6e9c30d1f29594d686382dd63a834bb61be/.env.example#L3-L5)
  - [or by mapping the `~/.aws` to the container](https://github.com/michael-riha/agentgateway/blob/69b8b6e9c30d1f29594d686382dd63a834bb61be/compose.yaml#L11)

## A simple Request to the LLM Model via proxy

```
curl 'http://0.0.0.0:3000/' --header 'Content-Type: application/json' --data ' {
  "model": "anthropic.claude-3-5-sonnet-20240620-v1:0",
  "messages": [
    {
      "role": "user",
      "content": "Tell me a story"
    }
  ]
}
'
```
Still even works with an empty model 🤷‍♂️
```
curl 'http://0.0.0.0:3000/' --header 'Content-Type: application/json' --data ' {
  "model": "",
  "messages": [
    {
      "role": "user",
      "content": "Tell me a story"
    }
  ]
}
'
```

## Using the ` inspector` 

> [!NOTE] 
> I did not yet succeed with MCP over `agentgateway` so for debuggign I just used
> `inspector` (needs to be on host network mode) <-> `everything`-server

Browser: `http://localhost:6274/` (host networking mode, otherwise it doesn't work)
- http://localhost:3001/mcp (streamable)
- http://localhost:3001/sse (sse)

### `streamable-http` seems like to proxy via `6277`

```
curl 'http://localhost:6277/mcp?url=http%3A%2F%2Flocalhost%3A3001%2Fmcp&transportType=streamable-http' \
  -H 'accept: application/json, text/event-stream' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{"sampling":{},"elicitation":{},"roots":{"listChanged":true}},"clientInfo":{"name":"mcp-inspector","version":"0.16.5"}},"jsonrpc":"2.0","id":0}'
```

#### Response:
```
event: message
data: {"jsonrpc":"2.0","id":0,"result":{"protocolVersion":"2025-03-26","capabilities":{"prompts":{},"resources":{"subscribe":true},"tools":{},"logging":{},"completions":{}},"serverInfo":{"name":"example-servers/everything","version":"1.0.0"}}}
```

##### Headers:
```
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Access-Control-Expose-Headers: mcp-session-id
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
mcp-session-id: 5f130863-32e2-420a-a747-9fa654e774ef
Date: Thu, 04 Sep 2025 07:09:28 GMT
Transfer-Encoding: chunked
```

Request all MCP Tools from (custom)`everything` (service: `mcp-everything`)

⚠️ Use the `mcp-session-id` you got returned from the initial request

```
curl 'http://localhost:6277/mcp?url=http%3A%2F%2Flocalhost%3A3001%2Fmcp&transportType=streamable-http' \
  -H 'accept: application/json, text/event-stream' \
  -H 'content-type: application/json' \
  -H 'mcp-session-id: 5f130863-32e2-420a-a747-9fa654e774ef' \
  --data-raw '{"method":"tools/list","params":{"_meta":{"progressToken":2}},"jsonrpc":"2.0","id":2}' ;
```