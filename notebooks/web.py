import os
import uuid
import json
import re
from os.path import join

def slugify(text):
    text = text.lower()
    return re.sub(r'[\W_]+', '-', text)

def for_website(altair_plot, nb_name=None, plot_name=None):
    save_dir = os.getenv("4CE_SAVE_FOR_WEB_DIR", None)
    should_save_for_web = (save_dir != None and str(save_dir) != '0')

    if nb_name == None:
        nb_name = str(uuid.uuid4())[:8]
    if plot_name == None:
        plot_name = str(uuid.uuid4())[:8]

    nb_name = slugify(nb_name)
    plot_name = slugify(plot_name)

    if should_save_for_web:

        vega_json = altair_plot.to_dict()

        plot_id = f"{nb_name}_{plot_name}"

        plot_out_file = f"plot_{plot_id}.json"

        with open(join(save_dir, plot_out_file), "w") as f:
            json.dump(vega_json, f)