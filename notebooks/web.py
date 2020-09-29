import os
import uuid
import json
import re
from os.path import join
import lineup_widget

def slugify(text):
    text = text.lower()
    return re.sub(r'[\W_]+', '-', text)

def for_website(plot, nb_name=None, plot_name=None, df=None):
    save_dir = os.getenv("C19_SAVE_FOR_WEB_DIR", None)
    should_save_for_web = (save_dir != None and str(save_dir) != '0')

    if nb_name == None:
        nb_name = str(uuid.uuid4())[:8]
    if plot_name == None:
        plot_name = str(uuid.uuid4())[:8]

    nb_name = slugify(nb_name)
    plot_name = slugify(plot_name)

    if should_save_for_web:

        if type(plot) == lineup_widget.lineup.LineUpWidget:
            plot_json = plot._data
        else:
            plot_json = plot.to_dict()

        plot_id = f"{nb_name}_{plot_name}"

        plot_out_file = f"plot_{plot_id}.json"
        df_out_file = f"data_{plot_id}.csv"

        with open(join(save_dir, plot_out_file), "w") as f:
            json.dump(plot_json, f)
        
        if df is not None:
            df.to_csv(join(save_dir, df_out_file))