# c19i2b2-notebooks
Jupyter Notebooks for c19i2b2 project.

## Development

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

Add data files inside this folder, and make sure to properly set the data directory in `constants.py`:

```python
DATA_DIR = join("..", "data")
```

Enter the notebook directory:

```sh
cd notebooks
```

Start Jupyter with the Python (or R) kernel:

```sh
conda activate c19i2b2-py # or c19i2b2-r
jupyter notebook
```