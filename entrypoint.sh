/usr/bin/env sh
# wrapper for docker entrypoint

exec docker-entrypoint.sh server --console-address ":9001" /data