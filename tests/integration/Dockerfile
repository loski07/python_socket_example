FROM python:3.9.4

COPY server.py .
COPY client.py .
COPY wrapper.sh .

RUN "./wrapper.sh"

#CMD ["bash -c 'echo ./output.txt'"]
CMD ["bash"]
