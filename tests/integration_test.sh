#!/bin/bash

python ../server/server.py &
sleep 5
python ./integration/client.py &
python ./integration/client.py &
python ./integration/client.py &
python ./integration/client.py &
python ./integration/client.py &
