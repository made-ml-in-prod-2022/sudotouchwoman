# __Production-ready ML project example__

## __Project structure__

```
└── ml_project
    ├── artifacts           <- Model pickles
    ├── configs             <- Configuration routines
    ├── data                <- Data fetching/reading routines
    ├── docs                <- Usage and examples
    ├── features            <- Feature preprocessing
    ├── metrics             <- Model performance dumps
    ├── models              <- Routines to train and inference models
    ├── notebooks           <- Jupyter notebooks
    ├── settings            <- Config entitites
    └── testing             <- Unit-tests
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
