import os
import webview
from generator.script_generator import generate_all
from pipeline_gui_builder.constants.block_definitions import BLOCK_CATEGORIES
from tkinter import filedialog


class Api:
    def choose_output_path(self):
        initial_dir = os.path.expanduser("./jobs/")
        path = filedialog.asksaveasfilename(
            defaultextension=".py",
            initialdir=initial_dir,
            initialfile="run.py",
            filetypes=[("Python Files", "*.py")],
        )
        return path or None

    def generate_script(self, pipeline, path, generate_local_files):
        if not path:
            return None

        folder = os.path.dirname(path)
        generate_all(pipeline, folder, generate_local_files)

        return os.path.join(folder, "run.py")

    def get_block_categories(self):
        return BLOCK_CATEGORIES


if __name__ == "__main__":
    api = Api()
    webview.create_window(
        "Pipeline GUI Builder", "web/index.html", width=1280, height=720, js_api=api
    )
    webview.start(debug=False)
