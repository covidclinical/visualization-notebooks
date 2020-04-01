# c19i2b2-notebooks
Jupyter Notebooks for c19i2b2 project.

## Development

### First time setup and installation

Set up git hook to clear notebook outputs before commit:

```sh
cp ./pre-commit.sh ./.git/hooks/pre-commit
chmod +x ./.git/hooks/pre-commit
```

Set up environments using conda:

```sh
conda env create -f environment.py.yml
conda env create -f environment.r.yml
```

To use real datasets, create a data folder:

```sh
mkdir data
```

Add data files inside this folder, and make sure to properly set the data directory in [`notebooks/constants.py`](https://github.com/hms-dbmi/c19i2b2-notebooks/blob/master/notebooks/constants.py#L4):

```python
DATA_DIR = join("..", "data")
```

### Running and editing notebooks

Enter the notebook directory:

```sh
cd notebooks
```

Start Jupyter with the Python (or R) kernel:

```sh
conda activate c19i2b2-py # or c19i2b2-r
jupyter notebook
```

## Troubleshooting

### Updating a conda environment

To add or remove a conda package, update the corresponding environment file. Then run

```sh
conda env update -f environment.py.yml # or environment.r.yml
```