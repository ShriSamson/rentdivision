import streamlit as st
import pandas as pd
import numpy as np
from robust_rental_harmony import rental_harmony

st.title("Robust Rental Harmony Calculator")

# Input fields
total_rent = st.number_input("Enter the total rent:", min_value=0.0, step=0.01, key="total_rent")
num_housemates = st.number_input("Enter the number of housemates/rooms:", min_value=1, step=1, key="num_housemates")

# Add checkbox for Google Sheets import
use_gsheets = st.checkbox("Import data from Google Sheets (only for publicly shared spreadsheets)")

# Initialize edited_price_data in session state
if 'edited_price_data' not in st.session_state:
    st.session_state.edited_price_data = None
    st.session_state.room_names = None

if use_gsheets:
    gsheet_url = st.text_input("Enter the publicly shared Google Sheets URL:")
    import_button = st.button("Import Data")

    if import_button and gsheet_url:
        try:
            # Extract the sheet ID from the URL
            sheet_id = gsheet_url.split('/')[5]
            url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv'

            # Read the CSV data directly into a DataFrame using pandas
            df = pd.read_csv(url)
            
            # Update num_housemates based on imported data
            num_housemates = len(df.columns) - 1  # Assuming first column is housemate names
            
            # Extract room names and housemate names
            st.session_state.room_names = df.columns[1:].tolist()
            housemate_names = df.iloc[:, 0].tolist()
            
            st.success("Data imported successfully!")
            st.subheader("Imported Room Prices:")
            st.dataframe(df.set_index(df.columns[0]))
            
            st.session_state.edited_price_data = df.set_index(df.columns[0]).astype(float)
            print(st.session_state.edited_price_data)
        except Exception as e:
            st.error(f"An error occurred while importing data: {str(e)}")
            st.warning("Make sure the Google Sheet is publicly shared and the URL is correct.")
else:
    if num_housemates > 0:
        # Create input fields for room names and housemate names
        st.session_state.room_names = [st.text_input(f"Enter name for Room {i+1}:", key=f"room_name_{i}") for i in range(num_housemates)]
        housemate_names = [st.text_input(f"Enter name for Housemate {i+1}:", key=f"housemate_name_{i}") for i in range(num_housemates)]

        # Create n x n table for room prices
        st.subheader("Enter room prices:")
        price_data = {room: [0.0] * num_housemates for room in st.session_state.room_names}
        df = pd.DataFrame(price_data, index=housemate_names)

        # Use st.data_editor to create an editable table for user input
        st.session_state.edited_price_data = st.data_editor(
            df,
            num_rows="fixed",
            key="price_table",
            column_config={name: st.column_config.NumberColumn(f"Price for {name}", min_value=0.0, max_value=float(total_rent), step=0.01) for name in st.session_state.room_names}
        )

if st.button("Calculate Rental Harmony", key="calculate_button_unique"):
    #print('test')
    print(st.session_state.edited_price_data)
    if st.session_state.edited_price_data is not None:
        # Convert edited_price_data to the format expected by rental_harmony
        df = st.session_state.edited_price_data.copy()
        df.columns = range(len(df.columns))

        # Run the Robust Rental Harmony algorithm
        (solution, envies, envy_free) = rental_harmony(total_rent, df)

        # Replace room numbers with room names in the solution
        solution['Room'] = solution['Room'].map(lambda x: st.session_state.room_names[x])
        envies.columns = st.session_state.room_names
        
        st.subheader("Price Data:")
        st.dataframe(st.session_state.edited_price_data)

        st.subheader("Solution:")
        st.dataframe(solution, key="solution_display")

        st.subheader("Envies:")
        st.dataframe(envies, key="envies_display")

        st.subheader("Envy-free:")
        st.write(envy_free, key="envy_free_display")

        st.success("Rental harmony calculated successfully!")
    else:
        st.warning("Please enter or import room price data before calculating.")
