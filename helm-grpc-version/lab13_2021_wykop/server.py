import grpc
from concurrent import futures
import time
import math
import pandas as pd
import csv
import os
import fasttext as ft

from protobuf import wykop_pb2
from protobuf import wykop_pb2_grpc
from pymongo import MongoClient
from pyspark.sql import SparkSession

import pyspark.sql.functions as F
from pyspark.ml.feature import StringIndexer
from pyspark.sql.functions import split, col
from pyspark.sql.types import DoubleType, ArrayType, IntegerType
from pyspark.ml.linalg import VectorUDT, Vectors

from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression


def str_to_list(string):
    if isinstance(string, list):
        return string
    v_list = string[1:-1].split(",")
    return list(map(float, v_list))


def write_to_csv():
    client = MongoClient("mongodb://root:example@mongo:27017/")
    db = client["wykopDB"]

    posts_collection = db["posts"]
    posts = posts_collection.find()

    texts = dict()
    with open("lab13_2021_wykop/mongoDB.csv", "w+") as file:
        writer = csv.writer(file)
        writer.writerow(posts[0].keys())

        for document in posts:
            if (
                document["text"] not in texts
                or texts[document["text"]]["reactions_num"] < document["reactions_num"]
            ):
                writer.writerow(document.values())
                texts[document["text"]] = document


def prepapre_data():
    spark = SparkSession.builder.appName("lab10").getOrCreate()
    df = (
        spark.read.option("header", True)
        .option("quote", '"')
        .option("escape", '"')
        .csv("./lab13_2021_wykop/mongoDB.csv")
    )

    df = add_label_preprocess(preprocess(df))

    train, test = df.randomSplit([0.8, 0.2])
    return train, test


def add_label_preprocess(df):
    df = df.withColumn("reactions_num", df["reactions_num"].cast(DoubleType()))

    # 5. add labels
    df = df.withColumnRenamed("reactions_num", "label")
    return df


def preprocess(df):
    # 1. hour column
    hour = F.udf(lambda x: int(x[11:13]), IntegerType())
    df = df.withColumn("hour", hour("date"))

    # 3. cast vectors to double
    remove_parentheses = F.udf(str_to_list, ArrayType(DoubleType()))
    df = df.withColumn("vector", remove_parentheses("vector"))

    seqAsVector = F.udf(lambda vs: Vectors.dense(vs), VectorUDT())
    df = df.withColumn("vector", seqAsVector("vector"))

    # 4. cast others
    df = df.withColumn("comments_num", df["comments_num"].cast(IntegerType()))

    return df


def train(train_df):
    assembler = VectorAssembler(
        inputCols=["comments_num", "vector", "hour"], outputCol="features"
    )

    lr = LogisticRegression(maxIter=10, regParam=0.001)
    pipeline = Pipeline(stages=[assembler, lr])

    model = pipeline.fit(train_df)

    return model


def predict(request):
    date = request.date
    text = request.text
    comments_num = request.comments_num

    vector = lang_model.get_sentence_vector(text).tolist()
    client_data = pd.DataFrame(
        [[date, vector, comments_num]], columns=["date", "vector", "comments_num"]
    )

    spark = SparkSession.builder.appName("lab10").getOrCreate()
    df = spark.createDataFrame(client_data)
    df = preprocess(df)

    predictions = model.transform(df)
    prediction = predictions.select("prediction").collect()[0]

    predicted_pluses = prediction.__getitem__("prediction")
    predicted_pluses_int = int(math.ceil(predicted_pluses))
    return predicted_pluses_int


class ModelService(wykop_pb2_grpc.ModelService):
    def Test(self, request, context):
        print("Got a call: " + request.text)
        pluses_predicted = predict(request)
        response = wykop_pb2.PredictedPluses()
        response.value = pluses_predicted
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

wykop_pb2_grpc.add_ModelServiceServicer_to_server(
        ModelService(), server)

lang_model = ft.load_model("./celery_app/model/clarin.kgr10.20.bin")

type = os.getenv("TYPE","csv")
if type != "csv":
    print("Loading csv...")
    write_to_csv()

print("Preparing data...")
train_df, test_df = prepapre_data()

print("Fitting model...")
model = train(train_df)

# from types import SimpleNamespace

# b = {"text": "John", "date": "2021-12-16 16:06:57", "comments_num": "12"}
# a = SimpleNamespace(**b)
# predict(a)

print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
