# __Production-ready ML project example__

## __Project structure__

```
<<<<<<< HEAD
├── k8s                 <- Kubernetes Manifests
│   └── docs
=======
>>>>>>> @{-1}
├── ml_project          <- ML pipeline (train + batch inference)
│   ├── configs         <- Configuration yaml files
│   ├── data            <- Data storage (raw + synthetic)
│   ├── docs            <- Usage and examples
│   ├── notebooks       <- Jupyter notebooks
│   ├── outputs         <- Hydra's outputs (created automatically)
│   ├── src             <- Pipeline package
│   │   ├── data        <- Data fetching/reading routines
│   │   ├── features    <- Feature extraction/preprocessing
│   │   ├── models      <- Routines to train and inference models
│   │   └── settings    <- Config entities
│   └── testing         <- Unit-testing routines
└── online_inference    <- Online inference (as a Flask app)
    ├── app
    │   ├── utils
    │   └── view        <- Routes + application factory
    ├── configs         <- Application settings
    ├── data
    └── env             <- .env files
```

## __Prerequisites__

Project was tested under python `3.8.10`, but is likely to operate
for newer language versions.
Make sure to install the dependencies in `requirements.txt` via `pip install -r requirements.txt` command.

## __Project overview__
`ml_project` directory contains the project with CLI application to manage data and feature processing, model creation and evaluation. The dataset used is Wisconsin Breast Cancer Dataset, [source](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic))

The project structure is inspired (to reasonable extent) by [datascience-cookiecutter template](https://drivendata.github.io/cookiecutter-data-science/). Some sections are not present, like references or `sphinx` build.

For configuration management of the project, `hydra` framework is utilized ([hydra's docs](https://hydra.cc/)). This expierence was pretty nice for me, as I have never tickled with `yaml` files seriously (except for `docker-compose` ones). Value interpolation is a decent and versatile feature!

I do not perform much EDA in this section for a number of reasons: I have already worked with this dataset once, and that last time I implemented PCA to prove
that the target variable (cancer type of the patient) is linearly separable ([notebook with nice graphs](https://colab.research.google.com/github/sudotouchwoman/math-misc/blob/main/notebooks/PCA-and-graph-clustering.ipynb)). All the features are already denoised and distributed without outliers. This time I aimed to design a pipeline capable of multiple optional steps, that is why transforms for categorical features are present, yet there are no actual categorical features in the dataset.

`online_inference` directory contains Flask web-application that implements REST API for inference.
As the model artifact requires additional dependencies from `ml_project`, the `src` directory with pipeline sources is copied to `online_inference` (in sake of simplicity and in order to reduce  potential headache with distribution. It is preferable to wrap shared dependencies into a distributed python package but in this example in seemed to bring too much overhead).
<<<<<<< HEAD

`k8s` directory contains manifests for Kubernetes in `yaml` format and docs with screenshots.
Cluster was hosted at `VK Cloud Solutions` and the container image used is the one built with `Docker` for application at `online_inference` section.
Keywords: `pod`, `ReplicaSet`, `Deployment`, `Service`, `Ingress`, `nginx`.
=======
>>>>>>> @{-1}
