# visualization-notebooks [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/covidclinical/visualization-notebooks/master)

Jupyter Notebooks for 4CE data visualizations.

## Development

### First time setup and installation

Set up git hook to clear notebook outputs before commit:

```sh
cp ./pre-commit.sh ./.git/hooks/pre-commit
chmod +x ./.git/hooks/pre-commit
```

Set up environments using Conda and enable Jupyter widgets:

```sh
conda env create -f environment.yml
conda env create -f environment.r.yml

jupyter nbextension enable --py --sys-prefix lineup_widget
```

To use real datasets, create a data folder:

```sh
mkdir data
```

Add data files inside this folder, and make sure to properly set the data directory in `notebooks/constants.py`:

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
conda activate 4ce # or 4ce-r
jupyter notebook # or jupyter lab
```

## Conversion from Altair to Vega-Lite for the Web

Plots created with [Altair](https://altair-viz.github.io/) can be converted to the [Vega-Lite](https://vega.github.io/vega-lite/) JSON format, which enables these plots to be used on the website.

To streamline this process, any plots that should be used on the website should be passed to the `for_website()` function (defined [here](https://github.com/hms-dbmi/c19i2b2-notebooks/blob/master/notebooks/web.py)).

In a notebook, this would look like:

```python
from web import for_website
```

```python
plot = alt.Chart(df).mark_point().encode(x='day',y='num_patients')

# Specify the notebook name, and give each plot a unique name.
for_website(plot, "Labs", "Lab Values by Site")

plot
```

By default, the `for_website` function does nothing.
Only when the environment variable `C19_SAVE_FOR_WEB_DIR` is set on your computer, will the output JSON files be generated.

This environment variable can be set like this:

```sh
export C19_SAVE_FOR_WEB_DIR=~/research/dbmi/covid/plots_for_website
```

## Troubleshooting

### Updating a conda environment

To add or remove a conda package, update the corresponding environment file. Then run

```sh
conda env update -f environment.yml # or environment.r.yml
```

## Exporting

To export a notebook to HTML, with only the outputs and no code, run:

```sh
jupyter nbconvert --to html --no-input path/to/notebook.ipynb
```
