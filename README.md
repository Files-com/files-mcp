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

### Restricting Local File Transfers

Optionally set `FILES_COM_LOCAL_ROOT` in your client's server environment to an existing absolute directory path, such as `/home/user/Documents`. Uploads can only read files within that directory and its children, and downloads can only write there. When the variable is omitted or empty, transfers can use any local path accessible to the server.

The server resolves `..` and symbolic links before checking each path. Relative transfer paths are resolved from the server's working directory and must still stay inside the configured directory. A download can create a new file in an existing directory within the boundary. A nonempty value must name an existing absolute directory; otherwise, the server will not start.

This setting applies to local transfer paths. Files.com paths continue to follow the API key's permissions.

```shell title="Start the server"
uvx files-com-mcp
```

```shell title="With the API key in the environment"
FILES_COM_API_KEY=your-api-key uvx files-com-mcp
```

```shell title="Restrict local uploads and downloads"
FILES_COM_API_KEY=your-api-key FILES_COM_LOCAL_ROOT=/home/user/Documents uvx files-com-mcp
```

## Using With Claude

Claude Desktop uses the Files.com Python MCP package to call the Files.com API from your machine. This setup supports local use over STDIO (standard input and output) only. For a network connection to MCP, use the [Files.com hosted MCP service](https://www.files.com/docs/integrations/model-context-protocol-mcp-server).

Claude Desktop reads its MCP servers from `claude_desktop_config.json`. Add the entry on the right under `mcpServers`, replace the `FILES_COM_API_KEY` value with a Files.com API key, and restart Claude Desktop. The [MCP quickstart](https://modelcontextprotocol.io/quickstart/user#2-add-the-filesystem-mcp-server) shows where the file lives on each operating system, walking through the same steps for another server.

The entry starts the server with `uvx`, so [uv](https://docs.astral.sh/uv/) has to be installed first; see [Installation](/python-mcp/overview/installation).

Once Claude has restarted, the Files.com tools appear in its tool list. [Tools](/python-mcp/overview/tools) lists them by category and explains why it pays to enable only the ones a task needs.

To restrict local uploads and downloads, optionally add `"FILES_COM_LOCAL_ROOT": "/home/user/Documents"` alongside `FILES_COM_API_KEY` in the `env` object, using an existing absolute directory on your machine. Restart Claude Desktop after changing it. See [Restricting Local File Transfers](/python-mcp/overview/installation#restricting-local-file-transfers) for details.

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

Files.com preserves the spelling of file and folder paths while comparing them using shared case and Unicode rules. Use the SDK comparison helpers when matching paths locally.
<div></div>

### Capitalization

Files.com uses case-insensitive path matching based on its fixed Unicode comparison map.

For example, the following paths have the same comparison key:

| Path Variant                          | Comparison Key              |
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

Use `/` between folder and file names, without leading or trailing slashes. SDK normalization helpers convert backslashes to `/`, remove duplicate separators, and discard exact `.` and `..` components. Discarding `..` leaves the preceding folder name intact.

| Input | Normalized path |
|-------|-----------------|
| `folder/subfolder/file.txt` | `folder/subfolder/file.txt` |
| `/folder/subfolder/file.txt` | `folder/subfolder/file.txt` |
| `folder/subfolder/file.txt/` | `folder/subfolder/file.txt` |
| `//folder//file.txt` | `folder/file.txt` |
| `folder/../file.txt` | `folder/file.txt` |

<div></div>

### Unicode and Path Comparison

Files.com compares paths using a fixed mapping shared by the server and SDKs. It treats case and many accent differences as equivalent: `Résumé.txt` and `resume.txt` identify the same file, as do `q` followed by a combining acute accent and `q`. The mapping also handles other equivalences, such as Hiragana and Katakana. Lowercasing or applying a standard Unicode normalization form alone does not reproduce these rules.

SDK comparison helpers normalize path separators and dot segments, then apply the bundled [versioned comparison map](https://github.com/Files-com/files-sdk-javascript/blob/master/shared/path_comparison.json). The [shared examples](https://github.com/Files-com/files-sdk-javascript/blob/master/shared/comparison_examples.json) give exact comparison results for integrations that implement their own matching. The map uses hexadecimal Unicode scalar values as keys: a missing entry preserves the character, an empty replacement removes it, and other replacements may contain several characters. Apply each replacement once without normalizing or lowercasing the result again.

Use comparison results only for matching. Send the original path spelling in API requests and preserve it for display and local filenames; comparison results can have a different spelling or length.

Trailing whitespace is significant for comparison. `report.txt` and `report.txt ` are different file paths, and SDK helpers preserve spaces, tabs, and newlines. Folder names cannot end in whitespace. See [Unicode Normalization](https://www.files.com/docs/files-and-folders/file-system-semantics/unicode-normalization) for the complete path rules.

<div></div>

## Workspaces

A Workspace groups files, users, groups, Partners, integrations, and workflows within a Files.com Site. An integration can provision a Workspace for a department or project and delegate its operation to a team without making that team Site Administrators. Every Site has a Default Workspace, with ID `0`; additional Workspaces have their own IDs and root folders.

Account membership, request context, and permission grants serve different purposes. Creating an account in a Workspace determines where it belongs. Selecting a Workspace determines which resources a request operates on. A permission grant determines what the caller can do there. Selecting a Workspace never grants access to it.

### Accounts and Administrative Access

A user's or group's `workspace_id` identifies the Workspace the account belongs to. Accounts belonging to a Custom Workspace stay within it. Default Workspace users and groups can receive permissions in one or more Custom Workspaces while keeping their existing accounts in Workspace `0`.

| Account | Workspace Administrator assignment | Scope |
| --- | --- | --- |
| User belonging to a Custom Workspace | Set the user's `workspace_admin` to `true`. | That user's own Custom Workspace. |
| Default Workspace user | Create an `admin` Permission for the user on a Custom Workspace's root folder. | Each Custom Workspace with a root grant. |
| Default Workspace group | Create an `admin` Permission for the group on a Custom Workspace's root folder. | Every member inherits administration of each Workspace with a root grant. |

`workspace_admin` is not a summary of a user's effective administrative access. A Default Workspace user can administer a Custom Workspace through a direct or group root grant while their `workspace_admin` remains `false`. Groups have no `workspace_admin` field. See [Users](https://developers.files.com/rest/resources/user-accounts/users) and [Groups](https://developers.files.com/rest/resources/user-accounts/groups) for account fields.

An `admin` grant on the **Custom Workspace root** provides full Workspace Administrator authority over its files, users, groups, Partners, workflows, and integrations. An `admin` grant on a subfolder provides Folder Admin authority over that folder and its descendants; it does not provide Workspace administration. Other permission levels provide their corresponding folder access without Workspace administration. [Permissions](https://developers.files.com/rest/resources/user-accounts/permissions) defines the levels.

Site Administrators manage cross-Workspace assignments to Default Workspace accounts. Workspace Administrators manage accounts and permissions within their own scope. Site Administrators retain access to every Workspace; adding a Workspace grant does not narrow Site Administrator authority. The [product documentation](https://www.files.com/docs/workspaces/workspace-administrators) explains the administrator's operational scope and site-wide controls.

### Request Context and API Keys

You can include the `X-Files-Workspace-Id` REST header to select a Workspace for a request. SDK request options and CLI configuration send that same selection. When a Workspace is selected, Workspace-scoped resources are listed, created, and changed within that context, and ordinary paths are relative to its root.

A resource's `workspace_id` request field describes the resource's Workspace membership. It is separate from the SDK's Workspace request option or REST header. Creating a Workspace-scoped resource in a Custom Workspace defaults its `workspace_id` to the selected Workspace; a mismatching membership value is rejected with `not-authorized/insufficient-permission-for-params`.

Selecting another Workspace with an API key requires a **Full Access key created in the Default Workspace**. A user key follows that user's current access, including group permissions. A site-wide Full Access key created in the Default Workspace has Site Administrator authority in every Workspace. A Files Only key stays in its creation Workspace, even if its user has cross-Workspace access. Any key created in a Custom Workspace stays within that Workspace. Selecting another context with these confined keys is rejected with `bad-request/invalid-workspace-id-header`.

An account belonging to a Custom Workspace is scoped there when it authenticates normally. For a Default Workspace user, explicitly select the intended Workspace for an integration rather than relying on an interactive login preference. [API Keys](https://developers.files.com/rest/resources/developers/api-keys) and [Authentication](https://developers.files.com/rest/overview/authentication) cover credentials.

The adjacent request uses the member's own Default Workspace Full Access user key to list the root of Workspace `123`, after access has been assigned.

```shell title="Request as the group member"
curl 'https://YOUR_SUBDOMAIN.files.com/api/rest/v1/folders/' \
  -H 'X-FilesAPI-Key: YOUR_MEMBER_API_KEY' \
  -H 'X-Files-Workspace-Id: 123'
```

### Delegating a Workspace to an Existing Group

An operations team already represented by a Default Workspace group can administer a Custom Workspace through one root Permission. The group and its members stay in the Default Workspace, so the same team can receive different access in other Workspaces.

First retrieve the target [Workspace](https://developers.files.com/rest/resources/settings/workspaces) and [Group](https://developers.files.com/rest/resources/user-accounts/groups) IDs as a Site Administrator in Workspace `0`. The examples use Workspace `123`, group `456`, and member user `789`; replace them with your own IDs. Confirm that the group belongs to Workspace `0` and that the intended user is a member.

Create the Permission using a Default Workspace Full Access site-wide key or a Full Access user key belonging to a Site Administrator. Keep the request context at `0` and use the qualified root path `_/Workspaces/123`. Set `group_id` to the group's ID, `permission` to `admin`, and `recursive` to `true`. Save the returned Permission `id` for later removal. For an individual Default Workspace user, use `user_id` instead of `group_id`.

For a Default Workspace group, a Site Administrator can also select Workspace `123` and use an empty `path` to grant access to its root. The qualified path in Workspace `0` works for both Default Workspace users and groups and keeps the account scope and target Workspace explicit. Appending a subfolder to the path would grant Folder Admin access instead of Workspace Administrator authority.

After the grant, make a request as the member, using their own credential with Workspace `123` selected, such as listing that Workspace's root folder. That member can work with the Workspace's files and perform Workspace Administrator operations, such as managing its users, Partners, and integrations. A Site Administrator's successful request does not establish that the member has the intended access.

```shell title="Find account and Workspace IDs"
curl 'https://YOUR_SUBDOMAIN.files.com/api/rest/v1/workspaces' \
  -H 'X-FilesAPI-Key: YOUR_SITE_ADMIN_API_KEY' \
  -H 'X-Files-Workspace-Id: 0'
curl 'https://YOUR_SUBDOMAIN.files.com/api/rest/v1/groups' \
  -H 'X-FilesAPI-Key: YOUR_SITE_ADMIN_API_KEY' \
  -H 'X-Files-Workspace-Id: 0'
```

```shell title="Grant group administration"
curl 'https://YOUR_SUBDOMAIN.files.com/api/rest/v1/permissions' \
  -X POST \
  -H 'X-FilesAPI-Key: YOUR_SITE_ADMIN_API_KEY' \
  -H 'X-Files-Workspace-Id: 0' \
  -H 'Content-Type: application/json' \
  -d '{"path":"_/Workspaces/123","group_id":456,"permission":"admin","recursive":true}'
```

### Permission Inspection and Removal

List the member's Permissions with `user_id` and `include_groups=true` to include grants inherited through group membership. Listing only direct user grants can miss the Permission that provides Workspace administration. In Workspace `0`, the Custom Workspace root appears as `_/Workspaces/123`; in Workspace `123`, paths are relative to that root. Inspect the root path and `permission=admin`, rather than treating the user's `workspace_admin` field as their effective administrative access.

Permission lists show individual grants, rather than a single flag for effective administrative access. Membership in several groups combines their access. A Permission using `group_ids` instead of `group_id` requires membership in all the specified groups; it is not a shorthand for assigning the same grant to several independent groups.

Removing a member ends access received through that group. Deleting the root Permission ends the group's Workspace Administrator grant for every member. These changes leave independent direct and other group grants in place, so review all applicable grants when withdrawing access. Default Workspace user API keys follow those permission changes without being recreated.

Group membership maintained through SCIM follows the same rule. A Group Admin allowed to add members can give those users the group's existing Workspace Administrator access. Choose who manages the group with that authority in mind.

Delete the Permission by its returned `id` as the Site Administrator in Workspace `0`. The removal examples use Permission ID `9001`; replace it with the ID returned by your create request. Permissions are created and deleted, rather than updated in place. If narrower folder access is still needed, assign it explicitly; deleting a broad grant does not restore narrower grants it previously replaced.

```shell title="Inspect member grants and remove the group grant"
curl 'https://YOUR_SUBDOMAIN.files.com/api/rest/v1/permissions?user_id=789&include_groups=true' \
  -H 'X-FilesAPI-Key: YOUR_SITE_ADMIN_API_KEY' \
  -H 'X-Files-Workspace-Id: 0'
curl 'https://YOUR_SUBDOMAIN.files.com/api/rest/v1/permissions/9001' \
  -X DELETE \
  -H 'X-FilesAPI-Key: YOUR_SITE_ADMIN_API_KEY' \
  -H 'X-Files-Workspace-Id: 0'
```

## Foreign Language Support

The Files.com MCP will soon be updated to support localized responses by using a configuration
method. When available, it can be used to guide the API in selecting a preferred language for applicable response content.

Language support currently applies to select human-facing fields only, such as notification messages
and error descriptions.

If the specified language is not supported or the value is omitted, the API defaults to English.

## Errors

## Mock Server

Files.com publishes a mock Files.com API server, which is useful for testing your use of the Files.com
SDKs and other direct integrations against the Files.com API in an integration test environment.
It never checks credentials: send any placeholder API key, and never use real Files.com credentials
with it.

The server has two modes, chosen when it starts:

* **Legacy mode** (the default) checks required parameters and parameter types, then returns a fixed
  example response for each API endpoint. It does not maintain state and it does not deeply inspect
  your submissions for correctness, which makes it useful for testing basic network operations and
  JSON encoding for your SDK or API client.
* **Simulation mode** keeps records, files and folders in memory, so a test can create, list, update
  and delete resources, upload a file and download the same bytes, and make chosen requests fail,
  stall or lose their connection on purpose. Requests it does not simulate fail with a clear error
  instead of returning an example response.

Start the server from its source with Ruby and Bundler. `FILES_MOCK_MODE` is read once at startup:
leaving it unset or setting it to `legacy` starts legacy mode, `simulation` starts simulation mode,
and any other value stops startup with an error. Legacy mode listens on port 4041 on all IPv4
interfaces, and simulation mode on `127.0.0.1:4041`.

Simulation mode keeps its state only in the server process. Its control endpoints under
`/__files_mock/v1` report when the server is ready, reset it with your fixtures, add fault rules
and return the journal of the requests it received. It refuses work over its limits instead of
truncating it. The README in the source describes all of these, the operations it simulates and
how to configure its limits.

Download the server as a Docker image via [Docker Hub](https://hub.docker.com/r/filescom/files-mock-server).
The image's `latest` tag moves to whichever server was published last, so it need not include
simulation mode; to run exactly the server the README describes, build the image from the source.

The Source Code is also available on [GitHub](https://github.com/Files-com/files-mock-server).

```shell title="Start the Mock Server"
bundle install

## Legacy mode
bundle exec puma

## Simulation mode
FILES_MOCK_MODE=simulation bundle exec puma
```

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
