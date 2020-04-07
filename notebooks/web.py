import os
import uuid
import json
import re
from os.path import join

def slugify(text):
    text = text.lower()
    return re.sub(r'[\W_]+', '-', text)

def for_website(altair_plot, nb_name=None, plot_name=None):
    save_dir = os.getenv("C19_SAVE_FOR_WEB_DIR", None)
    should_save_for_web = (save_dir != None and str(save_dir) != '0')

    if nb_name == None:
        nb_name = str(uuid.uuid4())[:8]
    if plot_name == None:
        plot_name = str(uuid.uuid4())[:8]

    nb_name = slugify(nb_name)
    plot_name = slugify(plot_name)

    if should_save_for_web:

        vega_json = altair_plot.to_dict()
        data = list(vega_json['data'].values())
        assert(len(data) == 1)

        dataset = list(vega_json['datasets'].values())[0]

        plot_id = f"{nb_name}_{plot_name}"

        data_out_file = f"data-{plot_id}.json"
        plot_out_file = f"plot-{plot_id}.json"

        with open(join(save_dir, data_out_file), "w") as f:
            json.dump(dataset, f)

        del vega_json['data']
        del vega_json['datasets']

        vega_json['data'] = {
            'url': data_out_file
        }
        with open(join(save_dir, plot_out_file), "w") as f:
            json.dump(vega_json, f)