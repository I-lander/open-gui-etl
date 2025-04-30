import os


def generate_all(pipeline, folder, generateLocalFiles):
    generate_script(pipeline, folder)
    if not folder or not generateLocalFiles:
        return
    os.makedirs(os.path.join(folder, "IN"), exist_ok=True)
    os.makedirs(os.path.join(folder, "OUT"), exist_ok=True)
    write_dot_env(pipeline, folder)


def generate_script(pipeline, folder):
    lines = [
        "import os",
        "import pandas as pd",
        "",
        "from utils.runner import *",
        "from utils.file_management import *",
        "from utils.data_management import *",
        "",
    ]

    for block in pipeline:
        if "s3" in block["type"] and "from utils.s3_utils import *" not in lines:
            lines.append("from utils.s3_utils import *")
        if (
            "rabbitmq" in block["type"]
            and "from utils.rabbitmq_utils import *" not in lines
        ):
            lines.append("from utils.rabbitmq_utils import *")
        if (
            "gdrive" in block["type"]
            and "from utils.gDrive_utils import *" not in lines
        ):
            lines.append("from utils.gDrive_utils import *")

    lines.append(
        "load_env(__file__)",
        "",
        'OUT = os.getenv("OUT")',
        'IN = os.getenv("IN")',
        "",
    )

    lines.append("")
    lines.append("def main():")

    for block in pipeline:
        lines.append("")
        lines.append(f"    # {block['type'].upper()}")
        for line in block["code"]:
            lines.append(f"{line}")

    lines += ["", "", 'if __name__ == "__main__":']

    lines.append("    run_main(main)")

    lines.append("")

    code = "\n".join(lines)
    path = f"{folder}/run.py"
    with open(path, "w") as f:
        f.write(code)
    return path


def write_dot_env(pipeline, folder_path):
    env_path = os.path.join(folder_path, ".env")
    with open(env_path, "w") as f:
        f.write("# JOB\nIN=\nOUT=\n")

        for block in pipeline:
            if "s3" in block["type"]:
                f.write("\n# S3\nAWS_ACCESS_KEY=\nAWS_SECRET_KEY=\nAWS_BUCKET=\n")
            if "rabbitmq" in block["type"]:
                f.write(
                    "\n# RabbitMQ\nRABBITMQ_HOST=\nRABBITMQ_PORT=\nRABBITMQ_USER=\nRABBITMQ_PASS=\nRABBITMQ_EXCHANGE=\n"
                )
            if "gdrive" in block["type"]:
                f.write(
                    "\n# Google Drive\nGDRIVE_CREDENTIALS_FILE=\nGDRIVE_FOLDER_ID=\n"
                )
