# The local-only Files.com MCP server, packaged with Python and its
# dependencies. It still speaks MCP over STDIO only: the MCP client starts the
# container with `docker run -i` (never -t) and the server exits when the
# client closes stdin. Nothing listens on a port. See README.md, "Running In
# Docker".
#
#   docker build -t files-com-mcp .
#
# FILES_COM_SDK_VERSION pins the released files-com SDK the image installs,
# for example --build-arg FILES_COM_SDK_VERSION=1.6.123. Without it the image
# installs the latest files-com release, as `pip install files-com-mcp` does.

ARG PYTHON_IMAGE=python:3.11-slim-bookworm

FROM ${PYTHON_IMAGE} AS build
WORKDIR /src
COPY . .
# This directory's package, not the files_com_mcp release on PyPI.
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels .

FROM ${PYTHON_IMAGE}
ARG FILES_COM_SDK_VERSION=
# The MCP Registry checks io.modelcontextprotocol.server.name against
# server.json's name before it lists an image.
LABEL org.opencontainers.image.title="Files.com MCP Server" \
      org.opencontainers.image.description="Local-only Files.com MCP server over STDIO" \
      org.opencontainers.image.source="https://github.com/Files-com/files-mcp" \
      org.opencontainers.image.licenses="MIT" \
      io.modelcontextprotocol.server.name="com.files/python-mcp"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HOME=/tmp \
    FILES_COM_LOCAL_ROOT=/work
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl \
        ${FILES_COM_SDK_VERSION:+"files-com==${FILES_COM_SDK_VERSION}"} \
    && rm -rf /wheels \
    && useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin mcp \
    && mkdir -p /work/uploads /work/downloads \
    && chown -R mcp:mcp /work
# Uploads and downloads are limited to /work: mount host folders at
# /work/uploads (read-only) and /work/downloads. HOME is /tmp so the image
# also runs under --user with the host's uid.
USER mcp
WORKDIR /work
ENTRYPOINT ["files-com-mcp"]
