# Files.com MCP Server

The `files-com-mcp` Python package lets your AI application interact with Files.com. It is for local use only and supports STDIO only: your MCP client starts the package as a subprocess on the same machine.

For MCP connections over a network, use the [Files.com hosted MCP service](https://www.files.com/docs/integrations/model-context-protocol-mcp-server).

Set `FILES_COM_API_KEY` in the environment your client passes to the subprocess. The local package makes outbound requests to the Files.com API to perform site operations.

Files.com is the cloud-native, next-gen MFT, SFTP, and secure file-sharing platform that replaces brittle legacy servers with one always-on, secure fabric. Automate mission-critical file flows—across any cloud, protocol, or partner—while supporting human collaboration and eliminating manual work.

With universal SFTP, AS2, HTTPS, and 50+ native connectors backed by military-grade encryption, Files.com unifies governance, visibility, and compliance in a single pane of glass.

## Introduction

The Files.com Python MCP package lets Claude Desktop and other local MCP clients upload and download files, query folders, manage users, and run automations on your Files.com site. It uses the permissions of your API key, and its actions are logged like those of any other API client.

The Python package supports local use over STDIO (standard input and output) only. Your MCP client starts it on the same machine and communicates directly with that process, without a network listener. The package still needs outbound access to the Files.com API.

### What MCP Is

The Model Context Protocol (MCP) is a standard interface through which a Large Language Model calls real APIs as part of its work. An MCP server hands the model a set of tools, and each Files.com tool is an authenticated operation in your site. With the server connected, the model can:

- Transfer files between cloud and on-premises systems
- Query folders and file metadata
- Create and manage users
- Automate workflows such as archiving or sharing

### Common Use Cases

**Assistants for operations teams.** An internal chatbot fetches or archives files on request.

**Automated workflows.** An agent reacts to an incoming support request, then retrieves or uploads the files the case needs.

**Developer copilots.** A development-focused LLM creates users, provisions folders, or reads files while debugging.

### Local vs. Hosted MCP

Use the [local Python package](/python-mcp/overview/installation) with clients that launch STDIO servers, including [Claude Desktop](/python-mcp/overview/using-with-claude).

For clients that connect to MCP over a network, use the [Files.com hosted MCP service](https://www.files.com/docs/integrations/model-context-protocol-mcp-server). Files.com operates the server, so you do not need to install the Python package. Running the Python package as an HTTP or SSE service is unsupported, including during development.

Install [uv](https://docs.astral.sh/uv/), register `uvx files-com-mcp` as an MCP server in your LLM client, and give it a Files.com API key in the `FILES_COM_API_KEY` environment variable.

```text title="Package"
https://pypi.org/project/files-com-mcp/
```

## Installation

The [`files-com-mcp`](https://pypi.org/project/files-com-mcp/) Python package lets your MCP client call the Files.com API through a process running on your machine. It supports local use over STDIO (standard input and output) only. For clients that connect to MCP over a network, use the [Files.com hosted MCP service](https://www.files.com/docs/integrations/model-context-protocol-mcp-server).

### Requirements

Your MCP client must be able to start a local STDIO server. Your machine needs outbound access to the Files.com API.

The examples run the server with `uvx`, which is part of [uv](https://docs.astral.sh/uv/). It runs a Python tool in an isolated environment of its own, so there is nothing to install or configure by hand beyond uv itself. Install uv first.

### Registering The Server

Set your client's local STDIO server command to `uvx` with `files-com-mcp` as the argument. `uvx` downloads the package on first use and starts it each time your client launches the server.

The [Claude Desktop configuration](/python-mcp/overview/using-with-claude) shows these settings in JSON. For other clients, follow their instructions for adding a local STDIO server.

### Authentication

The server authenticates to Files.com with an API key, read from the `FILES_COM_API_KEY` environment variable that your client passes to it. The model can do exactly what the key's user can do, so create a key for this purpose with the permissions the agent needs and no more.

```shell title="Start the server"
uvx files-com-mcp
```

```shell title="With the API key in the environment"
FILES_COM_API_KEY=your-api-key uvx files-com-mcp
```

## Using With Claude

Claude Desktop uses the Files.com Python MCP package to call the Files.com API from your machine. This setup supports local use over STDIO (standard input and output) only. For a network connection to MCP, use the [Files.com hosted MCP service](https://www.files.com/docs/integrations/model-context-protocol-mcp-server).

Claude Desktop reads its MCP servers from `claude_desktop_config.json`. Add the entry on the right under `mcpServers`, replace the `FILES_COM_API_KEY` value with a Files.com API key, and restart Claude Desktop. The [MCP quickstart](https://modelcontextprotocol.io/quickstart/user#2-add-the-filesystem-mcp-server) shows where the file lives on each operating system, walking through the same steps for another server.

The entry starts the server with `uvx`, so [uv](https://docs.astral.sh/uv/) has to be installed first; see [Installation](/python-mcp/overview/installation).

Once Claude has restarted, the Files.com tools appear in its tool list. [Tools](/python-mcp/overview/tools) lists them by category and explains why it pays to enable only the ones a task needs.

```json title="claude_desktop_config.json"
{
  "mcpServers": {
    "Files.com": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "files-com-mcp"
      ],
      "env": {
        "FILES_COM_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Tools

The Files.com MCP server exposes the tools below, grouped by category: files, folders, sharing, users, logs, automations and the other Files.com resources. Each tool is one operation in your site, run with the permissions of the API key the server holds.

### Keep The Toolset Focused

A model picks the right tool more reliably from a short list. If the LLM uses Files.com tools inconsistently, it is most likely choosing among too many. Most clients let you enable and disable an MCP server's tools one by one; enable only the ones the agent's task needs.

### Automations

| Tool | Description |
| ---- | ----------- |
| `Find_Automation` | Show Automation |
| `List_Automation` | List Automations |

### File System

| Tool | Description |
| ---- | ----------- |
| `Copy_File` | Copy File/Folder |
| `Create_Folder` | Create Folder |
| `Delete_File` | Delete File/Folder |
| `Find_File` | Find File/Folder by Path |
| `Gpg_Decrypt_File` | Decrypt a GPG-encrypted file and save it to a destination path. |
| `Gpg_Encrypt_File` | Encrypt a file with GPG and save it to a destination path. |
| `List_For_Folder` | List Folders by Path |
| `Move_File` | Move File/Folder |
| `Transform_File` | Transform a file and save the output to a destination path. |
| `Unzip_File` | Extract a ZIP file to a destination folder. |
| `Zip_File` | Create a ZIP from one or more paths and save it to a destination path. |
| `Zip_List_Contents_File` | List the contents of a ZIP file. |

### Integrations

| Tool | Description |
| ---- | ----------- |
| `Find_Remote_Server` | Show Remote Server |
| `List_Remote_Server` | List Remote Servers |

### Logging

| Tool | Description |
| ---- | ----------- |
| `List_Action_Log` | List Action Logs |
| `List_Api_Request_Log` | List API Request Logs |
| `List_Automation_Log` | List Automation Logs |
| `List_Email_Log` | List Email Logs |
| `List_Exavault_Api_Request_Log` | List Exavault API Request Logs |
| `List_External_Event` | List External Events |
| `List_File_Migration_Log` | List File Migration Logs |
| `List_For_File_History` | List history for specific file. |
| `List_For_Folder_History` | List history for specific folder. |
| `List_For_User_History` | List history for specific user. |
| `List_Ftp_Action_Log` | List FTP Action Logs |
| `List_History` | List site full action history. |
| `List_Inbound_S3_Log` | List Inbound S3 Logs |
| `List_Logins_History` | List site login history. |
| `List_Outbound_Connection_Log` | List Outbound Connection Logs |
| `List_Public_Hosting_Request_Log` | List Public Hosting Request Logs |
| `List_Scim_Log` | List Scim Logs |
| `List_Settings_Change` | List Settings Changes |
| `List_Sftp_Action_Log` | List SFTP Action Logs |
| `List_Sync_Log` | List Sync Logs |
| `List_Web_Dav_Action_Log` | List WebDAV Action Logs |

### Sharing / Share Links

| Tool | Description |
| ---- | ----------- |
| `Create_Bundle` | Create Share Link |
| `Create_Bundle_Notification` | Create Share Link Notification |
| `Create_Bundle_Recipient` | Create Share Link Recipient |
| `Delete_Bundle` | Delete Share Link |
| `Delete_Bundle_Notification` | Delete Share Link Notification |
| `Find_Bundle` | Show Share Link |
| `Find_Bundle_Notification` | Show Share Link Notification |
| `List_Bundle` | List Share Links |
| `List_Bundle_Download` | List Share Link Downloads |
| `List_Bundle_Notification` | List Share Link Notifications |
| `List_Bundle_Recipient` | List Share Link Recipients |
| `List_Bundle_Registration` | List Share Link Registrations |
| `Update_Bundle` | Update Share Link |
| `Update_Bundle_Notification` | Update Share Link Notification |

### User Accounts

| Tool | Description |
| ---- | ----------- |
| `Create_Group` | Create Group |
| `Create_Permission` | Create Permission |
| `Create_User` | Create User |
| `Delete_Group` | Delete Group |
| `Delete_Permission` | Delete Permission |
| `Delete_User` | Delete User |
| `Find_Group` | Show Group |
| `Find_User` | Show User |
| `List_Group` | List Groups |
| `List_Permission` | List Permissions |
| `List_User` | List Users |
| `Update_Group` | Update Group |
| `Update_User` | Update User |

## Authentication

The Files.com MCP uses API key authentication.

### Authenticate with an API Key

Authenticating with an API key is the recommended authentication method for most scenarios, and is
the method used in the examples on this site.

To use an API Key, first generate an API key from the [web
interface](https://www.files.com/docs/sdk-and-apis/api-keys) or [via the API or an
SDK](/python-mcp/resources/developers/api-keys).

Note that when using a user-specific API key, if the user is an administrator, you will have full
access to the entire API. If the user is not an administrator, you will only be able to access files
that user can access, and no access will be granted to site administration functions in the API.

Don't forget to replace the placeholder, `YOUR_API_KEY`, with your actual API key.

## Sort and Filter

Several of the Files.com API resources have list operations that return multiple instances of the
resource. The List operations can be sorted and filtered.

### Sorting

To sort the returned data, pass in the ```sort_by``` method argument.

Each resource supports a unique set of valid sort fields and can only be sorted by one field at a
time.

#### Special note about the List Folder Endpoint

For historical reasons, and to maintain compatibility
with a variety of other cloud-based MFT and EFSS services, Folders will always be listed before Files
when listing a Folder.  This applies regardless of the sorting parameters you provide.  These *will* be
used, after the initial sort application of Folders before Files.

### Filtering

Filters apply selection criteria to the underlying query that returns the results. They can be
applied individually or combined with other filters, and the resulting data can be sorted by a
single field.

Each resource supports a unique set of valid filter fields, filter combinations, and combinations of
filters and sort fields.

#### Filter Types

| Filter | Type | Description |
| --------- | --------- | --------- |
| `filter` | Exact | Find resources that have an exact field value match to a passed in value. (i.e., FIELD_VALUE = PASS_IN_VALUE). |
| `filter_prefix` | Pattern | Find resources where the specified field is prefixed by the supplied value. This is applicable to values that are strings. |
| `filter_gt` | Range | Find resources that have a field value that is greater than the passed in value.  (i.e., FIELD_VALUE > PASS_IN_VALUE). |
| `filter_gteq` | Range | Find resources that have a field value that is greater than or equal to the passed in value.  (i.e., FIELD_VALUE >=  PASS_IN_VALUE). |
| `filter_lt` | Range | Find resources that have a field value that is less than the passed in value.  (i.e., FIELD_VALUE < PASS_IN_VALUE). |
| `filter_lteq` | Range | Find resources that have a field value that is less than or equal to the passed in value.  (i.e., FIELD_VALUE \<= PASS_IN_VALUE). |

## Paths

Working with paths in Files.com involves several important considerations. Understanding how path comparisons are applied helps developers ensure consistency and accuracy across all interactions with the platform.
<div></div>

### Capitalization

Files.com compares paths in a **case-insensitive** manner. This means path segments are treated as equivalent regardless of letter casing.

For example, all of the following resolve to the same internal path:

| Path Variant                          | Interpreted As              |
|---------------------------------------|------------------------------|
| `Documents/Reports/Q1.pdf`            | `documents/reports/q1.pdf`  |
| `documents/reports/q1.PDF`            | `documents/reports/q1.pdf`  |
| `DOCUMENTS/REPORTS/Q1.PDF`            | `documents/reports/q1.pdf`  |

This behavior applies across:
- API requests
- Folder and file lookup operations
- Automations and workflows

See also: [Case Sensitivity Documentation](https://www.files.com/docs/files-and-folders/case-sensitivity/)

### Slashes

All path parameters in Files.com (API, SDKs, CLI, automations, integrations) must **omit leading and trailing slashes**. Paths are always treated as **absolute and slash-delimited**, so only internal `/` separators are used and never at the start or end of the string.

####  Path Slash Examples
| Path                              | Valid? | Notes                         |
|-----------------------------------|--------|-------------------------------|
| `folder/subfolder/file.txt`       |   ✅   | Correct, internal separators only |
| `/folder/subfolder/file.txt`      |   ❌   | Leading slash not allowed     |
| `folder/subfolder/file.txt/`      |   ❌   | Trailing slash not allowed    |
| `//folder//file.txt`              |   ❌   | Duplicate separators not allowed |

<div></div>

### Unicode Normalization

Files.com normalizes all paths using [Unicode NFC (Normalization Form C)](https://www.unicode.org/reports/tr15/#Norm_Forms) before comparison. This ensures consistency across different representations of the same characters.

For example, the following two paths are treated as equivalent after NFC normalization:

| Input                                  | Normalized Form       |
|----------------------------------------|------------------------|
| `uploads/\u0065\u0301.txt`             | `uploads/é.txt`        |
| `docs/Café/Report.txt`                 | `docs/Café/Report.txt` |

- All input must be UTF‑8 encoded.
- Precomposed and decomposed characters are unified.
- This affects search, deduplication, and comparisons across SDKs.

<div></div>

## Workspaces

A Workspace is a lightweight way to organize related resources inside a single Files.com Site.

Customers commonly group resources by project, department, client, or region. Workspaces provide a built-in structure for that grouping, so the UI can operate within a clear "workspace context" and admins can delegate management for a subset of resources without requiring full site-level isolation.

Every Site has an implicit Default workspace (ID `0`). Resources that are not explicitly assigned to a named workspace are considered part of the Default workspace.

### Using Workspaces with the REST API

To use Workspaces with the REST API, send the following request header:

```http
X-Files-Workspace-Id: <workspace_id>
```

This changes path mapping and "what you're looking at."

When the `X-Files-Workspace-Id` header is provided:

- List, show, update, and delete operations are constrained to that workspace for workspace-scoped models.
- Create operations default `workspace_id` to the scoped workspace when not explicitly provided.
- Attempts to provide a mismatching `workspace_id` are rejected with `not-authorized/insufficient-permission-for-params`.

This header only works for sitewide keys, or keys related to users with permissions to more than one workspace.
<div></div>

## Foreign Language Support

The Files.com MCP will soon be updated to support localized responses by using a configuration
method. When available, it can be used to guide the API in selecting a preferred language for applicable response content.

Language support currently applies to select human-facing fields only, such as notification messages
and error descriptions.

If the specified language is not supported or the value is omitted, the API defaults to English.

## Errors

## Mock Server

Files.com publishes a Files.com API server, which is useful for testing your use of the Files.com
SDKs and other direct integrations against the Files.com API in an integration test environment.

It is a Ruby app that operates as a minimal server for the purpose of testing basic network
operations and JSON encoding for your SDK or API client. It does not maintain state and it does not
deeply inspect your submissions for correctness.

Eventually we will add more features intended for integration testing, such as the ability to
intentionally provoke errors.

Download the server as a Docker image via [Docker Hub](https://hub.docker.com/r/filescom/files-mock-server).

The Source Code is also available on [GitHub](https://github.com/Files-com/files-mock-server).

A README is available on the GitHub link.

## Development

Run the Python MCP package locally over STDIO when developing or modifying tools. Upload and Download tools rely on the file system where the MCP is running. For network connections, use the [Files.com hosted MCP service](https://www.files.com/docs/integrations/model-context-protocol-mcp-server).

To test LLM tools we recommend a popular command-line program called `inspector`. This will start a WebUI on a local port, the output of the command will give you the link to the inspector GUI.
Ex: http://127.0.0.1:6274


### Development - STDIO

```
FILES_COM_API_KEY="dummyKey" npx @modelcontextprotocol/inspector uv run -m files_com_mcp
```


### Development Claude Config

```
{
  "mcpServers": {
    "Files.com": {
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

## MCP Registry Metadata

```
mcp-name: com.files/python-mcp
```
