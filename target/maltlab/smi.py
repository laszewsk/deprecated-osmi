import grpc
import json
import numpy as np
import os
import requests
import tensorflow as tf

from smartredis import Client

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
from tensorflow.keras.models import load_model

from models import models


class SMI:

    def __init__(self, model, hostport=None):
        """
        Initializes a new instance of the SMI class.
        
        Args:
            model (str): The model to be used.
            hostport (str, optional): The host and port information. Defaults to None.
        """
        self.hostport = hostport
        self.model = model

    def grpc(self, batch):
            """
            gRPC function for making predictions using a TensorFlow Serving model.

            Parameters:
                batch (list): List of input data for making predictions.

            Returns:
                inference (function): Function that performs the inference using the gRPC connection.
            """
            
            channel = grpc.insecure_channel(
                self.hostport,
                options=[('grpc.max_receive_message_length', 2147483647)])
            stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

            def inference(data):
                request = predict_pb2.PredictRequest()
                request.model_spec.name = self.model
                request.model_spec.signature_name = 'serving_default'
                mods = models(batch)
                data = np.array(data, dtype=mods[self.model]['dtype'])
                request.inputs[mods[self.model]['input_name']]. \
                    CopyFrom(tf.make_tensor_proto(data, shape=mods[self.model]['input_shape']))
                response = stub.Predict(request)
                return response

            return inference

    def resp_inference(self):
            """
            Perform inference using the specified client and return the output tensor.

            Returns:
                A tensor containing the output of the inference.
            """
            client = Client(address=self.hostport)

            def inference(data):
                client.put_tensor("input", data)
                client.run_model("model", "input", "output")
                return client.get_tensor("output")

            return inference

    def http(self):
            """
            Sends an HTTP POST request to the specified model for inference.

            Returns:
                A function that takes in data and sends it for inference.

            Example:
                >>> smi = SMI()
                >>> inference_fn = smi.http()
                >>> result = inference_fn(data)
            """
            
            method_name = ":predict"
            headers = {"content-type": "application/json"}
            url = "http://" + self.hostport + "/v1/models/" + self.model

            def inference(data):
                payload = json.dumps({"instances": data.tolist()})
                response = requests.post(url + method_name, data=payload, headers=headers)
                return response

            return inference

    def embedded(self, model_base_path):
        """
        Loads a pre-trained model from the specified base path and returns a function 
        that can be used for embedding data.

        Parameters:
            model_base_path (str): The base path where the pre-trained model is stored.

        Returns:
            function: A function that takes data as input and returns the embedded 
                      representation using the loaded model.
        """
        model = load_model(os.path.join(model_base_path, self.model, "1"), compile=False)
        return lambda data: model(data)
