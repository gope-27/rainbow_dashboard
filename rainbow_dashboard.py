import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd


#***********https://www.webfx.com/tools/emoji-cheat-sheet/***********
st.set_page_config(page_title="Rainbow", page_icon=":rainbow:",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("")
st.markdown("")


#***********https://icons.getbootstrap.com/ (for icon)******
selected = option_menu("Rainbow Dashboard", ["Sales Analysis", "Product Analysis", "Store Analysis", "Customer Analysis", "Inventory Analysis"],
                       icons=['graph-up-arrow', 'cart4',
                              "shop", 'people', 'door-open-fill'],
                       menu_icon="cast",  # for menu icon
                       default_index=1,  # optional
                       orientation="horizontal",

                       styles={
    "container": {"padding": "0!important", "background-color": "#fafafa"},
    # "icon": {"color": "orange", "font-size": "15px"},
    # "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "rose"},
})

#Read csv


@st.cache
def get_data_from_csv():
    df = pd.read_csv("Rainbow_Final_Dataset.csv"
                     )
    return df


df = get_data_from_csv()

with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if selected == "Store Analysis":

    col1, col2, col3, col4 = st.columns(4)

    with col1:
       # st.markdown("Select Branches")
        selection_box1 = st.selectbox("Select Branches",
                                          options=df["Branch"].unique())
    with col2:
        selection_box2 = st.selectbox("Select Channel",
                                          options=df["Channel"].unique())
    with col3:
        selection_box3 = st.selectbox("Select Weekday/Weekend",
                                          options=df["isWeekday"].unique())
    with col4:
        selection_box4 = st.selectbox("Select Date",
                                          options=df["Purchase_Date"].unique())
    df = get_data_from_csv()
    df_selection = df.query(
                "Branch == @selection_box1 & Channel == @selection_box2 & isWeekday == @selection_box3 & Purchase_Date == @selection_box4")
                                
    st.markdown("")
        
    #TOTALSALES
    total_sales = df_selection['Net Amount'].sum()

    #TOTAL_ORDERS
    total_orders = df_selection['Order number'].count()

   #Gross MARGIN
    gross_margin = (
                     (df_selection['Profit'].sum()/df_selection['Net Amount'].sum()) * 100).round()

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        if total_sales <= 999999:
            st.markdown("<h4 style='text-align: center; color: black;'>Total Sales</h4>", unsafe_allow_html=True)
        #st.markdown("<h4 style='text-align: center; color: #ff4b4c;'>"+str(round(total_sales  /1000000,2))+"M"+"</h4>", unsafe_allow_html=True) 
            #st.markdown("<h4 style='text-align: center; color: #ff4b4c;'>"+str(total_sales)+"</h4>", unsafe_allow_html=True)  
            st.markdown("<h4 style='text-align: center; color: #ff4b4c;'>"+str(round(total_sales/1000,2))+"k"+"</h4>", unsafe_allow_html=True) 
        elif total_sales >= 99999:
            st.markdown("<h4 style='text-align: center; color: #ff4b4c;'>"+str(round(total_sales  /1000000,2))+"M"+"</h4>", unsafe_allow_html=True)
            
    with middle_column:
                st.markdown("<h4 style='text-align: center; color: black;'>Total Orders</h4>", unsafe_allow_html=True)
                st.markdown("<h4 style='text-align: center; color: #ff4b4c;'>"+str(round(total_orders ))+"</h4>", unsafe_allow_html=True)
        
    with right_column:
                st.markdown("<h4 style='text-align: center; color: black;'>Gross Margin</h4>", unsafe_allow_html=True)
                st.markdown("<h4 style='text-align: center; color: #ff4b4c;'>"+str(gross_margin)+"%"+"</h4>", unsafe_allow_html=True)
