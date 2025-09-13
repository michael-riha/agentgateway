
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
    - for testing with an external MCP ✅
  - `ghcr.io/modelcontextprotocol/inspector`
    - for inspecting and debugging MCP interactions ✅
  - `echo`
    - for debugging and output of HTTP interaction via the gateway
  - ☝️**mcp-server** (`source code` [& dedicated `compose.yaml`](./compose.yaml#L1-L2))
    - a custom MCP Server example in `python` to be called over `agentgateway`
    - 👀 into the `./src`-folder it includes a custom MCP Server example <br><br> 
    A standalone tool for testing and debugging as well as an example Graph using LangGraph.
---

## Terminology

> In LangGraph, you are building a graph (the application). <br>
> The nodes are connected by edges (the transitions between steps).
> This graph is composed of nodes (the steps).
> One or more of these nodes can themselves be agents (intelligent, looping subsystems). 
> The graph is the boss that manages the agents and other workers.

### My Rule of Thumb

> If the node contains an LLM that is empowered to make decisions in a loop (typically using tools), it is an **agent node**. 
> If the node uses an LLM for a single, deterministic task, it's just an **"LLM" node**.
> If it has no LLM at all, it's a **function node**.

---

# Usage

` docker compose up`

## Exploring:

- http://localhost:6274/ (the MCP Inspector)
  - as URL you can use:
    - http://localhost:3000/graph (over the gateway)
    - http://localhost:8000/mcp (direct call the MCP Server)
  - Press **▶️ Connect**
    - goto: http://localhost:6274/#tools & Click "List Tools"
    - 👀 at the tools
- http://localhost:15000/ui (agentgateway UI)
  - goto: http://localhost:15000/ui/playground/
    - select a Route (MCP) & connect
    - see all Tools available

## Debugging & Learning

- Connect the VSC Debugger [*Python: Remote Attach to Graph Client*](./.vscode/launch.json#L22) to the `graph`-service (`./src/compose.yaml`)
  - set Breakpoints
  - watch the Graph being executed
    - Uses `agentgateway` for LLM calls over `aws Bedrock`
    - Uses the local MCP-Server examples for testing and debugging

### All works as expected if ...

```bash
... 
graph-1           | Tool calls: None
graph-1           | Response content: 8
...
```

## `aws` `bedrock` for `LLM`-routing

- [add config](./services_configs/agentgateway/ai-config.yaml#L15-L25)
  - OR/AND enable this config in the [compose.yaml](./compose.yaml#L16) file
- for the `aws`-credentials:
  - [either via ENV-vars (preferred)](./env.example#L3-L5)
  - [or by mapping the `~/.aws` to the container](./compose.yaml#L11)

## A simple Request to the LLM Model via proxy

```
curl 'http://0.0.0.0:3000/bedrock' --header 'Content-Type: application/json' --data ' {
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
curl 'http://0.0.0.0:3000/bedrock' --header 'Content-Type: application/json' --data ' {
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

## ` ollama` 

```bash
curl http://localhost:7869/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      {"role": "user", "content": "Which LLM Model are you?"}
    ],
    "stream": false
  }'
```


## `agentgateway`

```bash
curl http://localhost:3000/ollama/api/chat \
  -H "Content-Type: application/json"  \
  -d '{
    "model": "llama3.1",
    "messages": [
      {"role": "user", "content": "Which LLM Model are you?"}
    ],
    "stream": false
  }'
```

### OpenAI compatible
```bash
curl http://localhost:3000/ollama/v1/chat/completions \
  -H "Content-Type: application/json"  \
  -d '{
    "model": "llama3.1",
    "messages": [
      {"role": "user", "content": "Which LLM Model are you?"}
    ],
    "stream": false
  }'
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