# Files.com Python MCP Server

Files.com's MCP gives your LLM access to our most popular API operations.

## What Is MCP?

Model Context Protocol (MCP) is a protocol designed to expose structured tools or capabilities that can be incorporated into a Large Language Model (LLM)'s execution context. It allows LLMs, like ChatGPT or Claude, to call real-world functions as part of generating responses.

Think of MCP as a standardized way to present a set of available "tools" (functions) that an LLM can use when it doesn't just need to answer, but needs to act, e.g. uploading a file, querying a folder, or creating a user.

## Important Information

Some LLMs struggle with too many tools in the context. LLM clients often offer a way to disable and enable specific tools for an MCP. If your LLM is having trouble picking the right tools, try disabling the tools you do not need in your LLM client.

## Installing in Claude

To install into Claude you have to add JSON to the `claude_desktop_config.json`

An official tutorial can found here: https://modelcontextprotocol.io/quickstart/user#2-add-the-filesystem-mcp-server

To add our MCP, add the following JSON (be sure to change the path and FILESCOM_API_KEY value)

NOTE: This version assumes you are running from source. Once we have PyPi publishing this README will have them version as well.

### uv Required

These examples requires `uv` which is a popular modern environment manager for running isolated python tools. Installation is out of scope of this README.

### Claude Config - STDIO

```
{
  "mcpServers": {
    "files_com_mcp": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/folder-containing-files_com_mcp",
        "run",
        "-m",
        "files_com_mcp"
      ],
      "env": {
        "FILES_COM_API_KEY": "CHangeME"
      }
    }
  }
}
```

## Development

While our MCP works well out-of-the-box, some power users find value in modifying MCP code to suit their unique needs. For those power users, it is recommended to use STDIO mode. Upload and Download tools rely on the file system where the MCP is running.

To test LLM tools we recommend a popular command-line program called `inspector`. This will start a WebUI on a local port, the output of the command will give you the link to the inspector GUI.
Ex: http://127.0.0.1:6274

## Develoment - STDIO

```
FILESCOM_API_KEY="dummyKey" npx @modelcontextprotocol/inspector uv run -m files_com_mcp
```

## Development - SSE

```
FILESCOM_API_KEY="dummyKey" uv run -m files_com_mcp --mode server --port 12345
```

Launch the inspector

```
npx @modelcontextprotocol/inspector
```
