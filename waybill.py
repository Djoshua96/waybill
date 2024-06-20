import streamlit as st
import pandas as pd

st.title("Waybill Checker")

# Function to highlight duplicates and unique waybills
def highlight_waybills(waybills):
    highlighted_html = ""
    for wb in waybills:
        if waybills.count(wb) > 1:
            highlighted_html += f'<span style="color:green;">{wb}</span><br>'
        else:
            highlighted_html += f'<span style="color:red;">{wb}</span><br>'
    return highlighted_html

# Function to find unique waybills
def find_unique_waybills(waybills):
    return [wb for wb in waybills if waybills.count(wb) == 1]

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Read the uploaded Excel file
    df = pd.read_excel(uploaded_file)

    # Display the uploaded data
    st.write("File Uploaded")
    st.dataframe(df)

    # Display column names for user to select the waybill columns to match
    columns = df.columns.tolist()
    selected_columns = st.multiselect("Select the columns for waybill numbers you want to check:", columns)

    if len(selected_columns) == 2:
        # Extract waybill numbers from both columns and combine them
        waybill_numbers_col1 = df[selected_columns[0]].dropna().tolist()
        waybill_numbers_col2 = df[selected_columns[1]].dropna().tolist()
        combined_waybill_numbers = waybill_numbers_col1 + waybill_numbers_col2

        # Highlight the combined waybill numbers
        st.write("Extracted Waybill Numbers (duplicates in red, unique in green)")
        highlighted_waybills = highlight_waybills(combined_waybill_numbers)
        st.markdown(highlighted_waybills, unsafe_allow_html=True)

        # Find unique waybills
        unique_waybills = find_unique_waybills(combined_waybill_numbers)

        # Display unique waybills separately at the bottom
        st.write("Unique Waybills (appear only once across both columns)")
        st.write(unique_waybills)
    else:
        st.write("Please select exactly two columns for waybill numbers.")
