import pandas as pd
import os
def get_dcf_extract():
    dcf_file = "DCF_model_CBA_alex.xlsx"
    
    if os.path.exists(dcf_file):
        df = pd.read_excel(dcf_file)
        df = df.head(5)  # ← return the DataFrame, not string
        return df
    else:
        print("DCF_model.xlsx not found.")
        return pd.DataFrame()  # Return empty DataFrame if file not found
