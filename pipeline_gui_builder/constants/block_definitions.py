BLOCK_CATEGORIES = {
    "IN / OUT": [
        {
            "label": "Read Excel",
            "id": "read_excel",
            "description": "Search and read the Excel file in the IN folder. The folder will be editable.",
            "code": [
                "    # The parameter IN can be modified if the excel file is elsewhere",
                "    # The parameter header can also be changed to fit the excel file (0 is the first row, 1 is the second row, etc.)",
                "    # The parameter dtype can be added to adapt the column type. To force a column to be a string use the following line:",
                '    # df = pd.read_excel(get_excel_file(IN),header=0, dtype={"COLUMN_NAME": str}).fillna("")',
                "    df = pd.read_excel(get_excel_file(IN),header=0).fillna(" ")",
            ],
        },
        {
            "label": "Export Excel",
            "id": "write_excel",
            "description": "Write the Excel file in the OUT folder. The folder and file name will be editable.",
            "code": [
                "    # The parameter OUT can be modified if the excel file is elsewhere",
                "    # The parameter file_name can be modified to change the name of the file",
                "    file_name = 'file.xlsx'",
                '    outputFile = os.path.join(OUT, "file_name")',
                "    df.to_excel(outputFile, index=False)",
            ],
        },
    ],
    "Data Management": [
        {
            "label": "Filter",
            "id": "filter_rows",
            "description": "Apply filter to the rows. A filter column will be needed and a function to apply will also have to be set. <br>Example:<br> FILTERS = {'COLUMN_NAME': lambda value: value > 500000}",
            "code": [
                "    # Need to define the filter columns and the function to apply. Here, the row will filter the column 'COLUMN_NAME' where the value is different from empty string",
                '    # To filter on an empty date, you can use {"DATE_COLOMN": lambda value: pd.notna(value)}',
                '    FILTERS = {"COLUMN_NAME": lambda value: value != ""}',
                "    df = filter_rows(df, FILTERS)",
            ],
        },
        {
            "label": "Aggregate",
            "id": "aggregate_input",
            "description": "Apply aggregation to the rows. An aggregation column will be needed and a column to apply the sum will also have to be set. <br>Example:<br> GROUP_COLUMNS = ['COLUMN_1', 'COLUMN_2']<br>AMOUNT_COLUMN = 'COLUMN_3'",
            "code": [
                "    # Need to define the group columns and the column to apply the sum. Here, the row will group by the columns 'COLUMN_1' and 'COLUMN_2' and apply the sum on 'COLUMN_3'",
                '    GROUP_COLUMNS = ["COLUMN_1", "COLUMN_2"]',
                '    AMOUNT_COLUMN = "COLUMN_3"',
                "    df = aggregate_input(df, GROUP_COLUMNS, AMOUNT_COLUMN)",
            ],
        },
        {
            "label": "Mapping",
            "id": "map_rows",
            "description": "Apply a mapping to the rows using a predefined FIELD_MAPPING. Each field is transformed individually based on the input row.",
            "code": [
                "    # Define a dictionary that maps output field names to a transformation function",
                "    # Each function receives the current row and its index, and returns the mapped value",
                "    # The transformation function can be a lambda function or a regular function used in the lambda function",
                "    # Example:",
                "    # def build_description(row):",
                "    #     return f'{row['COLUMN_1']} - {row['COLUMN_2']}'",
                "    # FIELD_MAPPING:",
                "    # {",
                '    #     "ID": lambda row, row_index: row_index + 1,  # Assign an incremental ID starting from 1',
                '    #     "Description": lambda row, row_index: build_description(row),  # Copy and cast description field',
                '    #     "Total_Amount": lambda row, row_index: row["PRICE"] * row["QUANTITY"],  # Calculate total amount from price and quantity',
                '    #     "Trans_Date": lambda row, row_index: pd.to_datetime(row["DATE"]).strftime("%Y-%m-%d"),  # Format date field to YYYY-MM-DD',
                "    # }",
                "",
                "    # Actual FIELD_MAPPING used here",
                "    FIELD_MAPPING = {",
                '        "OutputFieldName": lambda row, row_index: str(row["InputFieldName"]),  # Map InputFieldName to OutputFieldName after casting to string',
                "    }",
                "",
                "    # Apply the mapping to the dataframe",
                "    df = map_fields(df, FIELD_MAPPING)",
            ],
        },
        {
            "label": "Fill Empty Fields",
            "id": "fill_empty_fields",
            "description": "Fill empty fields in the DataFrame. The column name will be editable.",
            "code": [
                "    # Need to define the column name to fill empty fields",
                '    column_name = ""',
                "    df = fill_empty_fields(df, column_name)",
            ],
        },
    ],
    "File Management": [
        {
            "label": "Clear Folder",
            "id": "clear_folder",
            "description": "Clear the folder. The folder will be editable.",
            "code": [
                "    # The parameter OUT can be modified to clear another folder",
                "    clear_folder(OUT)",
            ],
        },
        {
            "label": "Group Files In Single Folder",
            "id": "group_files_in_single_folder",
            "description": "Copy all files in a single folder. The folders from and where will be editable.",
            "code": [
                "    # The parameters IN and OUT can be modified to group files from another folder or to another folder",
                "    group_files_in_single_folder(IN, OUT)",
            ],
        },
        {
            "label": "Zip Folder",
            "id": "zip_Files",
            "description": "Zip all files in a single folder. The folders from and where will be editable.",
            "code": [
                "    # The parameter folder_path determines the folder to zip",
                "    folder_path = IN",
                "    # The parameter zip_path determines the path to save the zip file",
                "    zip_path = os.path.join(OUT, 'archive.zip')",
                "    zip_folder(folder_path, zip_path)",
            ],
        },
        {
            "label": "Unzip Folder",
            "id": "unzip_Files",
            "description": "Unzip all files in a single folder. The folders from and where will be editable.",
            "code": [
                "    # The parameter zip_path determines the path to the zip file",
                "    zip_path = os.path.join(IN, 'archive.zip')",
                "    # The parameter folder_path determines the folder to unzip",
                "    folder_path = OUT",
                "    unzip_folder(zip_path, folder_path)",
            ],
        },
    ],
    "RabbitMQ": [
        {
            "label": "Send Message",
            "id": "send_message_to_rabbitmq",
            "description": "Define a message and send a payload to RabbitMQ. ",
            "code": [
                "    rabbitmq_payload = {}",
                "    send_message_to_rabbitmq(rabbitmq_payload)",
            ],
        },
    ],
    "S3": [
        {
            "label": "Download File",
            "id": "download_file_on_s3",
            "description": "Download a file from S3. The variables will be loaded from the .env file.",
            "code": [
                "    # The parameter IN can be modified to download another in another folder.",
                "    # The parameter s3_prefix need to be set to determine where are the files in the S3 storage",
                '    s3_prefix = ""',
                "    download_s3_folder(IN, s3_prefix)",
            ],
        },
    ],
    "Google Drive": [
        {
            "label": "List Files",
            "id": "list_files_on_gdrive",
            "description": "List all files in a Google Drive folder. The variables will be loaded from the .env file.",
            "code": [
                "    # The parameter gdrive_folder_id can be set in the .env file to determine where are the files in the Google Drive storage",
                '    gdrive_folder_id = os.getenv("GDRIVE_FOLDER_ID")',
                "    list_files(gdrive_folder_id)",
            ],
        },
        {
            "label": "Download File",
            "id": "download_file_on_gdrive",
            "description": "Download a file from Google Drive. The variables will be loaded from the .env file.",
            "code": [
                "    # The parameter IN can be modified to download another in another folder.",
                "    # The parameter gdrive_folder_id need to be set to determine where are the files in the Google Drive storage",
                '    gdrive_folder_id = ""',
                "    download_file(gdrive_folder_id, IN)",
            ],
        },
        {
            "label": "Upload File",
            "id": "upload_file_on_gdrive",
            "description": "Upload a file to Google Drive. The variables will be loaded from the .env file.",
            "code": [
                "    # The parameter OUT can be modified to upload another in another folder.",
                "    # The parameter gdrive_folder_id need to be set to determine where are the files in the Google Drive storage",
                '    gdrive_folder_id = ""',
                "    upload_file(gdrive_folder_id, OUT)",
            ],
        },
        {
            "label": "Create Timestamped Folder",
            "id": "create_timestamped_folder_on_gdrive",
            "description": "Create a timestamped folder in Google Drive. The variables will be loaded from the .env file.",
            "code": [
                "    # The parameter OUT can be modified to create another in another folder.",
                "    # The parameter gdrive_folder_id need to be set to determine where are the files in the Google Drive storage",
                '    gdrive_folder_id = ""',
                "    create_timestamped_folder(gdrive_folder_id, OUT)",
            ],
        },
        {
            "label": "Move File",
            "id": "move_file_on_gdrive",
            "description": "Move a file in Google Drive. The variables will be loaded from the .env file.",
            "code": [
                "    # The parameter OUT can be modified to move another in another folder.",
                "    # The parameter gdrive_folder_id need to be set to determine where are the files in the Google Drive storage",
                '    gdrive_folder_id = ""',
                "    move_file(gdrive_folder_id, OUT)",
            ],
        },
    ],
}
