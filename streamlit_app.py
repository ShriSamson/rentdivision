import streamlit as st
import pandas as pd
import numpy as np
from robust_rental_harmony import rental_harmony

st.title("Robust Rental Harmony Calculator")

st.markdown("Credit for the algorithm goes to [acritch](https://github.com/critcha/rentdivision)")

# Instructions
st.markdown("""
**Instructions:**

Enter the names for the housemates and rooms, and have each housemate privately identify his/her least favorite room and write down a bid of $0 for that room. Next, have them privately write down how much extra they'd be willing to pay monthly (assuming they're playing close-to-average rent) for each other room. Then, reveal those values, enter them into the Marginal Values table below, and click "Calculate".
""")

# Display the total rent input and bind it to session state
st.number_input("Enter the total rent:", min_value=0.0, step=0.01, value=3500.0, key="total_rent")

# Add checkbox for Google Sheets import
use_gsheets = st.checkbox("Import data from Google Sheets (Recommended; only for publicly shared spreadsheets)")

# Initialize edited_price_data in session state
if 'edited_price_data' not in st.session_state:
    st.session_state.edited_price_data = None
    st.session_state.room_names = None

if use_gsheets:
    gsheet_url = st.text_input("Enter the publicly shared Google Sheets URL:", value="https://docs.google.com/spreadsheets/d/1NMh9PoxR5CAQ-p3zzhXMfsxs9o3tUQHVX9NwUY1iPag/edit?usp=sharing")
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
            
            st.session_state.edited_price_data = df.set_index(df.columns[0]).astype(float)
            print(st.session_state.edited_price_data)

            # Display the Imported Room Prices when import button is pressed
            st.subheader("Imported Room Prices:")
            st.dataframe(st.session_state.edited_price_data)
        except Exception as e:
            st.error(f"An error occurred while importing data: {str(e)}")
            st.warning("Make sure the Google Sheet is publicly shared and the URL is correct.")
else:
    num_housemates = st.number_input("Enter the number of housemates/rooms:", min_value=2, step=1, key="num_housemates")
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
            column_config={name: st.column_config.NumberColumn(f"Price for {name}", min_value=0.0, max_value=float(st.session_state.total_rent), step=0.01) for name in st.session_state.room_names}
        )

if st.button("Calculate Rental Harmony", key="calculate_button_unique"):
    print(st.session_state.edited_price_data)
    if st.session_state.edited_price_data is not None:
        # Convert edited_price_data to the format expected by rental_harmony
        df = st.session_state.edited_price_data.copy()
        df.columns = range(len(df.columns))

        # Run the Robust Rental Harmony algorithm
        (solution, envies, envy_free) = rental_harmony(st.session_state.total_rent, df)

        # Replace room numbers with room names in the solution
        solution['Room'] = solution['Room'].map(lambda x: st.session_state.room_names[x])
        envies.columns = st.session_state.room_names
        
        st.subheader("Solution:")
        st.dataframe(solution, key="solution_display")

        st.subheader("Envies:")
        st.markdown("""
        The Envies table is an estimate of how much the prices would have to change for a housemate to prefer a given room over their assigned room. Greater magnitudes indicate a larger price change needed in order to be envious, smaller negative values indicate someone is likely to be envious if only a small change in price or change in circumstance occurs.
        """)
        st.dataframe(envies, key="envies_display")

        st.subheader("Envy-free:")
        st.write(envy_free, key="envy_free_display")

        st.success("Rental harmony calculated successfully!")
    else:
        st.warning("Please enter or import room price data before calculating.")
