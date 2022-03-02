
import grpc
import sys
import argparse

from  protobuf import wykop_pb2
from  protobuf import wykop_pb2_grpc


channel = grpc.insecure_channel('localhost:50051')

stub = wykop_pb2_grpc.ModelServiceStub(channel)

parser = argparse.ArgumentParser()
parser.add_argument('--text', '-t', type=str, help='text', default="spam spam")
parser.add_argument('--date', '-d', type=str, help='date', default="2021-12-16 16:06:57")
parser.add_argument('--comments_n', '-c', type=str, help='number of comments', default="12")
args = parser.parse_args()

request = wykop_pb2.Post(text=args.text, date=args.date, comments_num=args.comments_n)

response = stub.Test(request)

print(response.value)