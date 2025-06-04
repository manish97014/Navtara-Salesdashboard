import os
import pandas as pd

# Paths
input_folder = r"C:\Users\Navtara- Surya\OneDrive - Meal Metrix\Navtara\Python- Sales Performance analysis\Reconciliations\Swiggy\swiggy_input"
output_file = r"C:\Users\Navtara- Surya\OneDrive - Meal Metrix\Navtara\Python- Sales Performance analysis\Reconciliations\Swiggy\output files\Swiggy source.xlsx"

# Keywords to match (case-insensitive partial match)
required_keywords = ['Order Date', 'Order Status', 'Order ID', 'Total Customer Paid']

# Initialize final data container
combined_data = []

# Recursively loop through all files in folder and subfolders
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            file_path = os.path.join(root, file)
            try:
                # Read the sheet from row 3 onward
                df = pd.read_excel(file_path, sheet_name='Order Level', skiprows=2)

                # Match required columns (partial and case-insensitive)
                matched_columns = []
                for keyword in required_keywords:
                    match = next((col for col in df.columns if keyword.lower() in str(col).lower()), None)
                    if match:
                        matched_columns.append(match)
                    else:
                        matched_columns.append(None)

                # If any required column is missing, skip the file
                if None in matched_columns:
                    print(f"⚠️ Skipping {file} due to missing columns.")
                    continue

                # Create filtered DataFrame with matched columns
                df_filtered = df[matched_columns].copy()
                df_filtered.columns = required_keywords  # Rename columns properly
                df_filtered['Source'] = file  # Add Source column

                # Append to combined list
                combined_data.append(df_filtered)

            except Exception as e:
                print(f"❌ Error processing file: {file} - {e}")

# Combine and export final output
if combined_data:
    final_df = pd.concat(combined_data, ignore_index=True)
    # Reorder columns
    final_df = final_df[['Order Date', 'Order Status', 'Order ID', 'Total Customer Paid', 'Source']]
    final_df.to_excel(output_file, index=False)
    print(f"✅ Extracted data saved to:\n{output_file}")
else:
    print("⚠️ No data found or matched in any files.")
