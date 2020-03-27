# c19i2b2-notebooks
Jupyter Notebooks for c19i2b2 project.

## Development

Set up environments using conda:

```sh
conda env create -f environment.py.yml
conda env create -f environment.r.yml
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