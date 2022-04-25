# __Basic usage__

## __Run the training pipeline with hydra__
In directory `ml_project`, run the following command:

```>>> python3 pipeline.py hydra/hydra_logging=none hydra.verbose=__main__```

After this, `outputs/` dir should be autoamtically created by hydra to manage runs.

__Note__: due to relative pathing, the paths convention is `../../../desired-dir-name`