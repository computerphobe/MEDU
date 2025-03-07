import pandas as pd
import os

# Folder containing all Excel files (each representing a different university)
folder_path = "./excel_merge/"  # Change this to your folder path
output_folder = os.path.join(folder_path, "merged_sheets")  # Folder for merged files

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all Excel files in the folder
for file in os.listdir(folder_path):
    if file.endswith(".xlsx") or file.endswith(".xls"):  # Ensure it's an Excel file
        file_path = os.path.join(folder_path, file)
        excel_data = pd.ExcelFile(file_path)

        # Read all sheets and store them in a list
        all_sheets = [excel_data.parse(sheet) for sheet in excel_data.sheet_names]

        # Merge all sheets of the current university file
        merged_df = pd.concat(all_sheets, axis=0, ignore_index=True)

        # Save the merged data to a new Excel file with the same name
        output_file = os.path.join(output_folder, f"merged_{file}")
        merged_df.to_excel(output_file, index=False)

        print(f"Merged sheets for {file} saved to {output_file}")

print("✅ All university sheets merged separately!")
