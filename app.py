import streamlit as st
import pandas as pd
import os
import pickle
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from utils import getMeanTopX_Int, getMeanTopX_SUI, collect_data, collect_data_No


### PAGE CONFIGURATION ###

st.set_page_config(
    page_title="Auswertungs-Dashboards",
    layout="wide",
    )

### PAGE CONTENT ###

st.title("FIS List Dashboard")

selected = option_menu(
            None, [ "Top 3", "Top 20", "Jahrgang Season", "Jahrgang Season No"],
            icons=["trophy-fill", "trophy", "trophy", "trophy"],
            orientation= "horizontal",
            styles={
                "container": {"padding": "0!important"},
                "icon": {"color": "rgb(0, 104, 201)", "font-size": "22px"},
                "nav-link": {"font-size": "22px", "text-align": "center", "margin":"0px",  "--hover-color": "#d6d6d6"},
                "nav-link-selected": {"background-color": "rgba(0, 104, 201, 0.5)", "font-weight": "normal", "color": "white"},
            })



### HELPER FUNCTIONS ###
def get_latest_fis_list():

    data = pd.read_csv("data/FIS-points-list-AL-2025-408.csv") 
    data.columns = map(str.lower, data.columns)

    return data

def highlight_suiss(val):
    if val == "SUI":
        return 'background-color: rgba(0, 102, 255, 0.8)'
    return ''


def formated_dataframe(df):

    df_formated = st.dataframe(
                    df,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Name": {"width": 150}
                    }
                )

    return df_formated

def create_table(data, discipline, n=3, style=False):

    pos = discipline + "pos"
    points = discipline + "points"

    df_filtered = data.dropna(subset=[pos])
    df_filtered = df_filtered.sort_values(by=pos, ascending=True)
    df_topX = df_filtered.head(n)

    # Format the table
    df_topX_display = df_topX.rename(columns={
        "competitorname": "Name",
        "nationcode": "Nat",
        points: "Best",
        pos: "Rank" 
    })[["Name", "Nat", "Best", "Rank"]]

    if style: 
        styled_df = (df_topX_display.style
                    .map(highlight_suiss, subset=['Nat'])
                    .format({
                        "Rank": "{:.0f}",   # No decimal places
                        "Best": "{:.2f}"    # Two decimal places
                    })
                )
        
        return formated_dataframe(styled_df)

    # Display the table in Streamlit
    return formated_dataframe(df_topX_display)




#------------------------------------------------------------TOP 3------------------------------------------------------------
if selected == "Top 3":

    st.title("FIS List 17th of 2025 (408 - 23-02-2025)")
    # Load the data (Change to read from pickle for easier solution)
    data = get_latest_fis_list()

    # Sort the data so the most recent year is at index 0 
    birthyear_options = data["birthyear"].unique().tolist()
    birthyear_options.sort(reverse=True)

    col1, col2, col3 = st.columns([1,1,2])

    with col1:
        option_birthyear = st.selectbox(
                                    "Birthyear",
                                    birthyear_options,
                                    index=0
                                )
    
    with col2:
        option_gender = st.selectbox(
                                    "Gender",
                                    ["M", "W"],
                                    index=0
                                )

    filtered_data = data[(data["birthyear"] == option_birthyear) & (data["gender"] == option_gender)]

    col2_1, col2_2, col2_3, col2_4 = st.columns([1,1,1,1])

    with col2_1:
        st.subheader("Slalom")
        create_table(filtered_data, "sl")

    with col2_2:
        st.subheader("Giant Slalom")
        create_table(filtered_data, "gs")

    with col2_3:
        st.subheader("Super G")
        create_table(filtered_data, "sg")

    with col2_4:
        st.subheader("Downhill")
        create_table(filtered_data, "dh")

    # Only swiss athletes
    col3_1, col3_2, col3_3, col3_4 = st.columns([1,1,1,1])
    SUI_data = filtered_data[filtered_data["nationcode"] == "SUI"]

    with col3_1:
        st.subheader("Slalom SUI")
        create_table(SUI_data, "sl")

    with col3_2:
        st.subheader("Giant Slalom SUI")
        create_table(SUI_data, "gs")

    with col3_3:
        st.subheader("Super G SUI")
        create_table(SUI_data, "sg")

    with col3_4:
        st.subheader("Downhill SUI")
        create_table(SUI_data, "dh")


    col4_1, col4_2, col4_3 = st.columns([1,1,2])

    with col4_1:
        option_birthyear2 = st.selectbox(
                                    "Birthyear",
                                    birthyear_options,
                                    key="by2",
                                    index=0
                                )
    
    with col4_2:
        option_gender2 = st.selectbox(
                                    "Gender",
                                    ["M", "W"],
                                    key="gen2",
                                    index=0
                                )
        
    filtered_data2 = data[(data["birthyear"] == option_birthyear2) & (data["gender"] == option_gender2)]

    col5_1, col5_2, col5_3, col5_4 = st.columns([1,1,1,1])

    with col5_1:
        st.subheader("Slalom")
        create_table(filtered_data2, "sl")

    with col5_2:
        st.subheader("Giant Slalom")
        create_table(filtered_data2, "gs")

    with col5_3:
        st.subheader("Super G")
        create_table(filtered_data2, "sg")

    with col5_4:
        st.subheader("Downhill")
        create_table(filtered_data2, "dh")

    # Only swiss athletes
    col6_1, col6_2, col6_3, col6_4 = st.columns([1,1,1,1])
    SUI_data2 = filtered_data2[filtered_data2["nationcode"] == "SUI"]

    with col6_1:
        st.subheader("Slalom SUI")
        create_table(SUI_data2, "sl")

    with col6_2:
        st.subheader("Giant Slalom SUI")
        create_table(SUI_data2, "gs")

    with col6_3:
        st.subheader("Super G SUI")
        create_table(SUI_data2, "sg")

    with col6_4:
        st.subheader("Downhill SUI")
        create_table(SUI_data2, "dh")


#------------------------------------------------------------TOP 20------------------------------------------------------------
if selected == "Top 20":

    data = get_latest_fis_list()

    # Sort the data so the most recent year is at index 0 
    birthyear_options = data["birthyear"].unique().tolist()
    birthyear_options.sort(reverse=True)

    col1, col2, col3 = st.columns([1,1,2])

    with col1:
        option_birthyear = st.selectbox(
                                    "Birthyear",
                                    birthyear_options,
                                    index=0
                                )
    
    with col2:
        option_gender = st.selectbox(
                                    "Gender",
                                    ["M", "W"],
                                    index=0
                                )
        
    filtered_data = data[(data["birthyear"] == option_birthyear) & (data["gender"] == option_gender)]

    col1_1, col1_2, col1_3, col1_4 = st.columns([1,1,1,1])

    with col1_1:
        st.subheader("Slalom")
        create_table(filtered_data, "sl", 20, True)

    with col1_2:
        st.subheader("Giant Slalom")
        create_table(filtered_data, "gs", 20, True)

    with col1_3:
        st.subheader("Super G")
        create_table(filtered_data, "sg", 20, True)

    with col1_4:
        st.subheader("Downhill")
        create_table(filtered_data, "dh", 20, True)

    
    st.subheader("SUI Athletes only")

    col2_1, col2_2, col2_3, col2_4 = st.columns([1,1,1,1])
    SUI_data = filtered_data[filtered_data["nationcode"] == "SUI"]

    with col2_1:
        st.subheader("Slalom")
        create_table(SUI_data, "sl", 5)

    with col2_2:
        st.subheader("Giant Slalom")
        create_table(SUI_data, "gs", 5)

    with col2_3:
        st.subheader("Super G")
        create_table(SUI_data, "sg", 5)

    with col2_4:
        st.subheader("Downhill")
        create_table(SUI_data, "dh", 5)



#------------------------------------------------------------Jahrgang Season------------------------------------------------------------
if selected == "Jahrgang Season":

    st.title("FIS Points List - Dashboard")

    # User inputs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        birthyear = st.number_input("Enter birth year:", value=1998, min_value=1994, max_value=2011)
    
    with col2:
        FISYear = st.number_input("Enter FIS Year:", value=1, min_value=1, max_value=5)
    
    with col3:
        Gender = st.selectbox("Select Gender:", options=['M', 'W'])
    
    with col4:
        disciplin = st.selectbox("Select Discipline:", options=['DH', 'SL', 'GS', 'SG', 'AC'])

    # Load the data
    pickle_file_path = 'fis_list_combined_export.pkl'
    if os.path.exists(pickle_file_path):
        with open(pickle_file_path, 'rb') as f:
            combined_df = pickle.load(f)
    else:
        st.error(f"Pickle file not found at {pickle_file_path}")

    #st.write(combined_df)
    combined_df['Listname'] = combined_df['Listname'].astype(str)
    combined_df['Listyear'] = combined_df['Listname'].str[-4:]
    combined_df['Listyear'] = combined_df['Listyear'].replace("4/25", "2025")

    # Collect data for top 3, 10, and 15
    df_results_top3 = collect_data(birthyear, FISYear, Gender, 3, disciplin, combined_df)
    df_results_top10 = collect_data(birthyear, FISYear, Gender, 10, disciplin, combined_df)
    df_results_top15 = collect_data(birthyear, FISYear, Gender, 15, disciplin, combined_df)

    # Display results
    #st.subheader('Top 3 Results')
    #st.write(df_results_top3)

    #st.subheader('Top 10 Results')
    #st.write(df_results_top10)

    #st.subheader('Top 15 Results')
    #st.write(df_results_top15)

    df_results_top3['Season'] = df_results_top3['Season'].astype(str) + "BY" + df_results_top3['birthyear'].astype(str)
    df_results_top10['Season'] = df_results_top10['Season'].astype(str) + "BY" + df_results_top10['birthyear'].astype(str)
    df_results_top15['Season'] = df_results_top15['Season'].astype(str) + "BY" + df_results_top15['birthyear'].astype(str)

    # Plotting
    fig, ax = plt.subplots(1, 3, figsize=(24, 6), dpi=300)  # Set dpi to 300 for higher resolution
    col1, col2, col3 = st.columns(3)
    with col1:
        # Top 3 Plot
        ax[0].plot(df_results_top3['Season'], df_results_top3['MeanInt'], label='Int', marker='o', color= '#0328fc')
        ax[0].plot(df_results_top3['Season'], df_results_top3['MeanSUI'], label='SUI', marker='o', color= '#4a0a13')
        ax[0].set_title('Top 3 ' + str(disciplin))
        ax[0].invert_yaxis()
        ax[0].set_xlabel('Season')
        ax[0].set_ylabel('Weltranglistenposition')
        ax[0].legend()
        ax[0].grid(True)
        ax[0].set_xticks(df_results_top3['Season'])  # Add tick for every year
        ax[0].set_xticklabels(df_results_top3['Season'], rotation=45)

    with col2:
        # Top 10 Plot
        ax[1].plot(df_results_top10['Season'], df_results_top10['MeanInt'], label='Int', marker='o', color= '#0328fc')
        ax[1].plot(df_results_top10['Season'], df_results_top10['MeanSUI'], label='SUI', marker='o', color= '#4a0a13')
        ax[1].set_title('Top 10 ' + str(disciplin))
        ax[1].invert_yaxis()
        ax[1].set_xlabel('Season')
        ax[1].set_ylabel('Weltranglistenposition')
        ax[1].legend()
        ax[1].grid(True)
        ax[1].set_xticks(df_results_top10['Season'])  # Add tick for every year

    with col3:
        # Top 15 Plot
        ax[2].plot(df_results_top15['Season'], df_results_top15['MeanInt'], label='Int', marker='o', color= '#0328fc')
        ax[2].plot(df_results_top15['Season'], df_results_top15['MeanSUI'], label='SUI', marker='o', color= '#4a0a13') 
        ax[2].set_title('Top 15 ' + str(disciplin))
        ax[2].invert_yaxis()
        ax[2].set_xlabel('Season')
        ax[2].set_ylabel('Weltranglistenposition')
        ax[2].legend()
        ax[2].grid(True)
        ax[2].set_xticks(df_results_top15['Season'])  # Add tick for every year
  

    st.pyplot(fig)

#------------------------------------------------------------Jahrgang Season No------------------------------------------------------------
if selected == "Jahrgang Season No":

    st.title("FIS Points List - Dashboard")

  # User inputs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        birthyear = st.number_input("Enter birth year:", value=1998, min_value=1994, max_value=2011)
    
    with col2:
        FISYear = st.number_input("Enter FIS Year:", value=1, min_value=1, max_value=5)
    
    with col3:
        Gender = st.selectbox("Select Gender:", options=['M', 'W'])
    
    with col4:
        disciplin = st.selectbox("Select Discipline:", options=['DH', 'SL', 'GS', 'SG', 'AC'])

    # Load the data
    pickle_file_path = 'fis_list_combined_export.pkl'
    if os.path.exists(pickle_file_path):
        with open(pickle_file_path, 'rb') as f:
            combined_df = pickle.load(f)
    else:
        st.error(f"Pickle file not found at {pickle_file_path}")

    #st.write(combined_df)
    combined_df['Listname'] = combined_df['Listname'].astype(str)
    combined_df['Listyear'] = combined_df['Listname'].str[-4:]
    combined_df['Listyear'] = combined_df['Listyear'].replace("4/25", "2025")


    df_results_top = collect_data_No(birthyear, FISYear, Gender, disciplin, combined_df)

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df_results_top.style.format(precision=0))

    with col2:
    
        # Create bar plot
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.25
        index = df_results_top['Season']
        bar1 = ax.bar(index, df_results_top['Top30'], bar_width, label='Top 30', color='#F5921B')
        bar2 = ax.bar(index + bar_width, df_results_top['Top50'], bar_width, label='Top 50', color='#87BB62' )
        bar3 = ax.bar(index + 2 * bar_width, df_results_top['Top70'], bar_width, label='Top 70', color='#876FD4')

        ax.set_xlabel('Season')
        ax.set_ylabel('Count')
        ax.set_title('Number of SUI Athletes in Top 30, 50, and 70')
        ax.set_xticks(index + bar_width)
        ax.set_xticklabels(df_results_top['Season'])
        ax.legend()
        ax.grid(False)

        st.pyplot(fig)

