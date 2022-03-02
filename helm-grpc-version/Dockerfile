FROM godatadriven/pyspark

ENV TYPE="csv"

WORKDIR /jobs/

ADD requirements.txt ./requirements.txt
ADD ./celery_app/model ./celery_app/model
ADD ./lab13_2021_wykop ./lab13_2021_wykop

RUN apt-get update
RUN apt-get install g++ -y
RUN pip install -r requirements.txt
# RUN python -m grpc_tools.protoc -I. --python_out=lab13_2021_wykop --grpc_python_out=lab13_2021_wykop protobuf/wykop.proto

EXPOSE 50051

ENTRYPOINT python ./lab13_2021_wykop/server.py

#docker run -v $(pwd)/lab13_2021_wykop:/jobs/lab13_2021_wykop -p 50051:50051 --rm  -it  --entrypoint bash lab13
#docker run -v $(pwd)/lab13_2021_wykop:/jobs/lab13_2021_wykop -p 50051:50051 -it lab13

#-t              : Allocate a pseudo-tty
#-i              : Keep STDIN open even if not attached
#-it For interactive processes (like a shell)