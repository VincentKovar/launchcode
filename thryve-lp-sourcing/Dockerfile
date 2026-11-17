# Adapted from LaunchCodeEducation/LaunchCodeAgenticEngineer module_1/Dockerfile
# for the thryve-lp-sourcing Target Codebase.
#
# Changes from the course starter:
# - Base project dependency install uses uv (this project's actual package
#   manager) against pyproject.toml/uv.lock, instead of pip + requirements.txt.
# - Everything else (agent tooling, ngrok, Claude Code config, entrypoint)
#   is unchanged from the course starter.

FROM python:3.12-slim
WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    curl \
    git \
    bash \
    ca-certificates \
    nano \
    procps \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install uv (this project's package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Project dependencies. Copied separately from the rest of the source so
# Docker can cache this layer when only application code changes.
# README.md is required here too: pyproject.toml declares it as the package
# readme, and hatchling (the build backend) fails without it present.
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --extra dev

# Install Claude Code
RUN npm install -g @anthropic-ai/claude-code

# Install OpenCode
RUN npm install -g opencode-ai

# Install ngrok
RUN curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | tee /etc/apt/sources.list.d/ngrok.list \
    && apt-get update && apt-get install -y ngrok \
    && rm -rf /var/lib/apt/lists/*

# Claude Code configuration: default settings + status line
RUN mkdir -p /root/.claude
COPY settings.json /root/.claude/settings.json
COPY statusline.sh /root/.claude/statusline.sh
RUN chmod +x /root/.claude/statusline.sh

# Copy entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Shell quality-of-life improvements
RUN echo 'export PS1="thryve-lp-sourcing:\\w# "' >> /root/.bashrc && \
    echo 'alias ll="ls -alF"' >> /root/.bashrc && \
    echo 'alias la="ls -A"' >> /root/.bashrc && \
    echo 'alias l="ls -CF"' >> /root/.bashrc && \
    echo 'alias python="python3"' >> /root/.bashrc && \
    echo 'alias pip="pip3"' >> /root/.bashrc

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]
