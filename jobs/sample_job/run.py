import os
import pandas as pd

from utils.runner import *
from utils.file_management import *
from utils.data_management import *

load_env(__file__)

OUT = os.getenv("OUT")
IN = os.getenv("IN")


def main():

    # CLEAR_FOLDER
    # The parameter OUT can be modified to clear another folder
    clear_folder(OUT)

    # READ_EXCEL
    # The parameter IN can be modified if the excel file is elsewhere
    # The parameter header can also be changed to fit the excel file (0 is the first row, 1 is the second row, etc.)
    # The parameter dtype can be added to adapt the column type. To force a column to be a string use the following line:
    # df = pd.read_excel(get_excel_file(IN),header=0, dtype={"COLUMN_NAME": str}).fillna("")
    df = pd.read_excel(get_excel_file(IN), header=0).fillna()

    # FILTER_ROWS
    # Need to define the filter columns and the function to apply. Here, the row will filter the column 'COLUMN_NAME' where the value is different from empty string
    # To filter on an empty date, you can use {"DATE_COLOMN": lambda value: pd.notna(value)}
    FILTERS = {"COLUMN_NAME": lambda value: value != ""}
    df = filter_rows(df, FILTERS)

    # AGGREGATE_INPUT
    # Need to define the group columns and the column to apply the sum. Here, the row will group by the columns 'COLUMN_1' and 'COLUMN_2' and apply the sum on 'COLUMN_3'
    GROUP_COLUMNS = ["COLUMN_1", "COLUMN_2"]
    AMOUNT_COLUMN = "COLUMN_3"
    df = aggregate_input(df, GROUP_COLUMNS, AMOUNT_COLUMN)

    # MAP_ROWS
    # FIELD_MAPPING = {
    #     "ID": lambda row, row_index: row_index + 1,
    #     "Description": lambda row, row_index: str(row["COLUMN_DESCRIPTION"]),
    #     "Total_Amount": lambda row, row_index: row["PRICE"] * row["QUANTITY"],
    #     "Trans_Date": lambda row, row_index: pd.to_datetime(row["DATE"]).strftime("%Y-%m-%d"),
    # }

    # --- Define your field mapping here ---
    FIELD_MAPPING = {
        "OutputFieldName": lambda row, row_index: str(row["InputFieldName"]),
    }
    df = map_fields(df, FIELD_MAPPING)

    # WRITE_EXCEL
    # The parameter OUT can be modified if the excel file is elsewhere
    # The parameter file_name can be modified to change the name of the file
    file_name = "file.xlsx"
    outputFile = os.path.join(OUT, file_name)
    df.to_excel(outputFile, index=False)

    # SEND_MESSAGE_TO_RABBITMQ
    from utils.rabbitmq_utils import send_message_to_rabbitmq

    rabbitmq_payload = {}
    send_message_to_rabbitmq(rabbitmq_payload)


if __name__ == "__main__":
    run_main(main)
