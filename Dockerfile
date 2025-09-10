FROM python:3.8-alpine

ENV PORT=8080

ENV CONFIG_FILE_LOCATION=/app/config.toml

RUN mkdir /app

WORKDIR /app

# Copy the application source code and setup files
COPY setup.py setup.cfg MANIFEST.in README.md ./
COPY alertmanager_gchat_integration/ ./alertmanager_gchat_integration/
COPY scripts/entrypoint.sh ./

# Install the application from the local source
RUN pip --no-cache-dir install .

CMD ["./entrypoint.sh"]
