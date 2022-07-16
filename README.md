# MNIST Web app

This repository contains a simple web app for making predictions using the MNIST dataset. The purpose is to understand torchserve and how to combine it with a webservice. The model for making the predictions has been downloaded from https://github.com/pytorch/serve/tree/master/examples/image_classifier/mnist/mnist_cnn.pt

## Torchserve only

In the repo https://github.com/pytorch/serve/tree/master/examples/image_classifier/mnist/ an example how to serve this model using a customized handler based on the ImageClassifier. I used the BaseHandler to get familiar with it. The handler script is called mnist_handler_base.py and I used this post to write it: https://towardsdatascience.com/deploy-models-and-create-custom-handlers-in-torchserve-fc2d048fbe91. The base handler script can be found here: https://github.com/pytorch/serve/blob/master/ts/torch_handler/base_handler.py

Create the ```.mar``` file, which contains all information to deploy the model (in order to execute this some dependencies need to be installed)
 ```torch-model-archiver --model-name mnist --version 2.0 --model-file mnist.py --serialized-file mnist_cnn.pt --handler mnist_handler_base.py --force```

Move the created file into the ```model-store``` folder

 ```mv mnist.mar model-store/```

Use docker to serve the model

```
docker run --rm -it -p 8080:8080 -p 8081:8081 --name mar -v $(pwd)/model-store:/home/model-server/model-store -v $(pwd):/home/model-server/examples pytorch/torchserve:latest torchserve --start --model-store model-store --models mnist=mnist.mar
```

Check which models are registered:

```curl http://127.0.0.1:8081/models/```

 output
```
{
  "models": [
    {
      "modelName": "mnist",
      "modelUrl": "mnist.mar"
    }
  ]
}
```

Make predictions: 
```curl http://127.0.0.1:8080/predictions/mnist -T 3.png```, output  ```3```

## Web-App
now we want to combine the above with a simple web app to make the predictions from an uploaded image:

* in folder ```deployment``` is a Dockerfile from ```pytorch/torchserve:latest```, which only copies the ```.mar``` file to the ```model-store``` folder. nd starts torchserve (Note: change latest to other version)
    * build the image: ```build -t torchserve-mar:v1```
* In subfolder ```app```
    * create file ```app.py``` and subfolders ```templates``` and ```static```
    * ```templates``` contains html content of app
    * ```static``` is for saveig the uploaded images
    * ```app.py``` is script that creates the app to make predictions
    * in folder ```app``` create Dockerfile to run the app
    * build the image ```docker-build -t app:v1```
* in folder ```deployment``` use ```docker-compose.yaml``` to run both services
* start services with ```docker-compose up```

