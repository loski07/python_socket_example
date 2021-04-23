#!/bin/bash

cp ../../server/server.py .
cp ../../client/client.py .
touch wrapper.sh
chmod +x wrapper.sh
echo -e "#!/bin/bash" >> wrapper.sh
echo -e "python ./server.py & > ./output.txt" >> wrapper.sh
echo -e "python ./client.py &" >> wrapper.sh

docker --config /tmp/.docker build -t python-socket-example .

#docker run -ti python-socket-example
#docker rm python-socket-example

rm server.py client.py wrapper.sh
