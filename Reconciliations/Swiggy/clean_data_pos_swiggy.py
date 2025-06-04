import os
import pandas as pd

# ---------- Paths ----------
input_folder = r"C:\Users\Navtara- Surya\OneDrive - Meal Metrix\Navtara\Python- Sales Performance analysis\Reconciliations\Swiggy\pos_input_swiggy"
output_file = r"C:\Users\Navtara- Surya\OneDrive - Meal Metrix\Navtara\Python- Sales Performance analysis\Reconciliations\Swiggy\output files\Swiggy POS.xlsx"

# ---------- Required Headers ----------
required_keywords = ['Deployment', 'Order Id', 'Bill Date', 'Gross Bill Amount']

# ---------- Data Collector ----------
combined_data = []

# ---------- Loop through files ----------
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.lower().endswith(('.xlsx', '.xls', '.csv')):
            file_path = os.path.join(root, file)
            try:
                # ✅ Read file, skip first 5 rows (header is at row 6)
                if file.lower().endswith('.csv'):
                    df = pd.read_csv(file_path, skiprows=5)
                else:
                    df = pd.read_excel(file_path, skiprows=5)

                # ✅ Match headers case-insensitively
                matched_columns = []
                for keyword in required_keywords:
                    match = next((col for col in df.columns if keyword.lower() in str(col).lower()), None)
                    matched_columns.append(match)

                # ❌ Skip if any required column is missing
                if None in matched_columns:
                    print(f"⚠️ Skipping '{file}' due to missing headers. Found: {matched_columns}")
                    continue

                # ✅ Filter and rename
                df_filtered = df[matched_columns].copy()
                df_filtered.columns = required_keywords
                df_filtered['Source'] = file

                # ✅ Remove rows where Deployment is "Grand Total" (case-insensitive) and blank rows
                df_filtered = df_filtered[~df_filtered['Deployment'].astype(str).str.lower().str.strip().eq('grand total')]
                df_filtered = df_filtered.dropna(subset=required_keywords)  # Remove rows with any missing values

                combined_data.append(df_filtered)

            except Exception as e:
                print(f"❌ Error in '{file}': {e}")

# ---------- Export ----------
if combined_data:
    final_df = pd.concat(combined_data, ignore_index=True)
    final_df = final_df[['Deployment', 'Order Id', 'Bill Date', 'Gross Bill Amount', 'Source']]
    final_df.to_excel(output_file, index=False)
    print(f"\n✅ Extracted data saved to:\n{output_file}")
else:
    print("⚠️ No matching data found in any files.")
