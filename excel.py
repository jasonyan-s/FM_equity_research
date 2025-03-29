import os
import pandas as pd

def get_dcf_extract():
    dcf_file = "DCF_model.xlsx"
    
    if os.path.exists(dcf_file):
            df = pd.read_excel(dcf_file)
            # Extract first 5 rows as a sample extract
            table_content = df.head(5).to_string(index=False)
            
            # # Print the table to terminal
            # print("\nDCF Model Table:")
            # print("-" * 50)
            # print(table_content)
            # print("-" * 50)


table_content = get_dcf_extract()  