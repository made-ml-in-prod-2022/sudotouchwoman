# __Production-ready ML project example__

`ml_project` directory contains the project with CLI application to manage data and feature processing, model creation and evaluation. The dataset used is Wisconsin Breast Cancer Dataset, [source](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic))

The project structure is inspired (to reasonable extent) by [datascience-cookiecutter template](https://drivendata.github.io/cookiecutter-data-science/). Some sections are not present, like references or `sphinx` build.

For configuration management of the project, `hydra` framework is utilized ([hydra's docs](https://hydra.cc/)). This expierence was pretty nice for me, as I have never tickled with `yaml` files seriously (except for `docker-compose` ones). Value interpolation is a decent and versatile feature!

I do not perform much EDA in this section for a number of reasons: I have already worked with this dataset once, and that last time I implemented PCA to prove
that the target variable (cancer type of the patient) is linearly separable ([notebook with nice graphs](https://colab.research.google.com/github/sudotouchwoman/math-misc/blob/main/notebooks/PCA-and-graph-clustering.ipynb)). All the features are already denoised and distributed without outliers. This time I aimed to design a pipeline capable of multiple optional steps, that is why transforms for categorical features are present, yet there are no actual categorical features in the dataset.