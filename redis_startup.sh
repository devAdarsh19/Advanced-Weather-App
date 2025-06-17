#!/bin/bash

# if pgrep "redis-server" > /dev/null
# then
#     echo "redis server already running"
# else
#     echo "Redis server not found. Attempting to start"

#     redis-server &> /dev/null &

#     sleep 2

#     if redis-cli ping &> /dev/null
#     then
#         echo "redis server started successfully"
#     else
#         echo "ERROR: Redis server failed to start or respond"
#         exit 1
#     fi
# fi

if redis-cli ping | grep -q PONG; then
    echo "Redis running"
else
    echo "ERROR: Redis server failed to connect"
    exit 1
fi
