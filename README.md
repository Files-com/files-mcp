# Files.com MCP Server

Files.com MCP allows your AI model, like ChatGPT or Claude, to use Files.com.

Files.com is the cloud-native, next-gen MFT, SFTP, and secure file-sharing platform that replaces brittle legacy servers with one always-on, secure fabric. Automate mission-critical file flows—across any cloud, protocol, or partner—while supporting human collaboration and eliminating manual work.

With universal SFTP, AS2, HTTPS, and 50+ native connectors backed by military-grade encryption, Files.com unifies governance, visibility, and compliance in a single pane of glass.

## Introduction

Modern AI models like ChatGPT and Claude are no longer just answering questions—they’re taking action. With Files.com MCP, you can securely give LLMs controlled access to real-world operations inside your Files.com environment.

Whether it's uploading, downloading, querying folders, or managing users, MCP enables your AI agent to interact with your Files.com infrastructure as if it were an extension of your team—without compromising on security, auditability, or control.

### What Is MCP?

Model Context Protocol (MCP) is a structured interface that lets Large Language Models call real APIs as part of their workflow. Think of it as a way to “hand tools” to the LLM—where the tools are real, authenticated functions from your Files.com environment.

When integrated via MCP, your LLM can:

 - Transfer files between cloud and on-prem systems

 - Query folders or file metadata

 - Create and manage users

 - Automate workflows like archival or sharing

 - And much more

MCP turns the LLM from a passive assistant into an active file operations agent.

### What is Files.com?

Files.com is the modern platform for secure file transfer, automation, and storage integration. Used by thousands of enterprises, Files.com connects cloud apps, on-prem systems, and human workflows—all through a single, powerful interface.

With robust APIs, native protocol support (SFTP, FTPS, AS2, and more), and enterprise-grade access controls, Files.com is built to move your files—reliably, securely, and at scale.

### Common Use Cases

*AI Assistants for Operations Teams:* Let your internal chatbot fetch or archive files on request.

*Automated LLM Workflows:* Build AI agents that react to incoming support requests, then retrieve or upload the necessary files from your environment.

*Developer Copilots:* Enable your dev-focused LLMs to create users, provision folders, or debug via real-time file access.

### Important Information

Large Language Models perform best when their toolset is focused. If you're integrating with Files.com MCP and noticing inconsistent tool usage, your LLM may be overloaded with too many available functions.

Most LLM clients allow you to selectively enable or disable tools exposed through MCP. For best results, only include the specific tools your agent needs for its task. This reduces ambiguity and improves the model’s ability to pick the right operation every time.

### Installation Into Your LLM

Each LLM client has its own method for installing an MCP, and they typically provide specific instructions. Many clients follow a pattern similar to Claude, so our Claude example is a great starting point if you’re working with one of those.

For LLMs that require a more detailed or technical setup, our MCP is implemented in Python and available on PyPI: https://pypi.org/project/files-com-mcp/

If your LLM client needs you to supply execution details for our MCP, we recommend using `uvx`, as demonstrated in the Claude example. This approach ensures a smooth, reproducible setup with minimal effort.

### Hosted MCP Server

Files.com also provides a hosted MCP server that lets AI agents connect to Files.com securely, without requiring you to run the Python package locally. For more information, see the [Files.com AI integrations](https://www.files.com/docs/integrations/ai) documentation.

### Using with Claude

To install into Claude you have to add JSON to the `claude_desktop_config.json` file

An official tutorial can found here: https://modelcontextprotocol.io/quickstart/user#2-add-the-filesystem-mcp-server

To add the Files.com MCP, use the Claude Config JSON below (be sure to change the FILES_COM_API_KEY value)

#### uv Required

These examples require `uv` which is a popular modern environment manager for running isolated python tools. You will need to install it first. Using uvx is a huge improvement over older Python environment setup methods. It is simple, runs smoothly, and eliminates the need for manual configuration or unnecessary complexity.

#### Claude Config

```
{
  "mcpServers": {
    "Files.com": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "files-com-mcp"
      ],
      "env": {
        "FILES_COM_API_KEY": "CHangeME"
      }
    }
  }
}
```

### Available Tools

The Files.com MCP provides tools for working with files, folders, sharing, users, logs, automations, and related Files.com resources.

#### Automations

| Tool | Description |
| ---- | ----------- |
| `Find_Automation` | Show Automation |
| `List_Automation` | List Automations |

#### File System

| Tool | Description |
| ---- | ----------- |
| `Copy_File` | Copy File/Folder |
| `Create_Folder` | Create Folder |
| `Delete_File` | Delete File/Folder |
| `Find_File` | Find File/Folder by Path |
| `List_For_Folder` | List Folders by Path |
| `Move_File` | Move File/Folder |
| `Unzip_File` | Extract a ZIP file to a destination folder. |
| `Zip_File` | Create a ZIP from one or more paths and save it to a destination path. |
| `Zip_List_Contents_File` | List the contents of a ZIP file. |

#### Integrations

| Tool | Description |
| ---- | ----------- |
| `Find_Remote_Server` | Show Remote Server |
| `List_Remote_Server` | List Remote Servers |

#### Logging

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

#### Sharing / Share Links

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

#### User Accounts

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
<div></div>

### SDK Support

We are still in the process of adding Workspaces support to each SDK. If you require Workspaces support right now, you need to use the REST API.
<div></div>

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

While our MCP works well out-of-the-box, some power users find value in modifying MCP code to suit their unique needs. For those power users, it is recommended to use STDIO mode. Upload and Download tools rely on the file system where the MCP is running.

To test LLM tools we recommend a popular command-line program called `inspector`. This will start a WebUI on a local port, the output of the command will give you the link to the inspector GUI.
Ex: http://127.0.0.1:6274


### Development - STDIO

```
FILES_COM_API_KEY="dummyKey" npx @modelcontextprotocol/inspector uv run -m files_com_mcp
```


### Development - SSE

```
uv run -m files_com_mcp --mode server --port 12345
```

When calling the SSE server, include `x-filesapi-key: <your-api-key>` as an HTTP header.
You can still set `FILES_COM_API_KEY` as a fallback when a header is not provided.

Launch the inspector

```
npx @modelcontextprotocol/inspector
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
