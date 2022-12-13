import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

#***********https://www.webfx.com/tools/emoji-cheat-sheet/***********
st.set_page_config(page_title="Rainbow", page_icon=":rainbow:",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("")
st.markdown("")


#***********https://icons.getbootstrap.com/ (for icon)******
selected = option_menu("Rainbow Dashboard", ["Sales Analysis", "Delivery Analysis", "Store Analysis", "Customer Analysis", "Inventory Analysis"],
                       icons=['graph-up-arrow', 'truck',
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

# with open('style.css') as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if selected == "Store Analysis":
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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
    #df = get_data_from_csv()
    df_selection = df.query(
                "Branch == @selection_box1 ")#& Channel == @selection_box2 & isWeekday == @selection_box3 & Purchase_Date == @selection_box4")
                                
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
            st.markdown("<h4 style='text-align: center; color: black;'>Total Sales</h4>", unsafe_allow_html=True)
            if total_sales <= 999999:
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

    #  Chart1
    st.markdown("<h4 style='text-align: left; color: black;'>Weekday/Weekend Order Count</h4>", unsafe_allow_html=True)
    df_avg_bu=df.groupby(["isWeekday"],as_index=False)['Order number'].sum()
    fig = go.Figure(data=[go.Pie(labels=df_avg_bu['isWeekday'], values=df_avg_bu['Order number'],hole=.5)])         
    fig.update_layout(height=500,width=600)

    # #chart2
    st.markdown("<h4 style='text-align: right; color: black;'>Channelwise Order Count</h4>", unsafe_allow_html=True)
    df_avg_bu=df.groupby(["Channel"],as_index=False)['Order number'].sum()
    fig1 = go.Figure(data=[go.Pie(labels=df_avg_bu['Channel'], values=df_avg_bu['Order number'],hole=.5)])        
    fig1.update_layout(height=500,width=600)

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig, use_container_width=True)
    right_column.plotly_chart(fig1, use_container_width=True)

    #Chart3
    df1 = df.groupby(['Branch']).agg({'Net Amount':'sum','Total Cost':'sum'}).reset_index()
    fig_hourly_sales = px.bar(
    data_frame = df1,
    x = "Branch",
    y = ["Net Amount","Total Cost"],
    opacity = 0.9,
    orientation = "v",
    barmode = 'group',
    title='<b>Branch Performance<b>',
    )
    fig_hourly_sales.update_layout(height=650,width=1500,xaxis_title="Salary in Million",
    yaxis_title="Business Unit",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)
    #fig_hourly_sales.update_traces(marker_color="#fb7373")

    st.plotly_chart(fig_hourly_sales, use_container_width=True)

    #chart-4
    df_se = df.groupby(['Branch']).agg({'Order number':'count','Channel':'count'}).reset_index()
    fig_hourly = px.bar(
    data_frame = df_se,
    x = "Branch",
    y = ["Order number","Channel"],
        
    orientation = "v",
    barmode = 'stack',
    title='<b>Branch Performance through Channel<b>',
    color_discrete_sequence=["#0083B8"]
    )
    fig_hourly_sales.update_layout(height=650,width=1500,xaxis_title="Salary in Million",
    yaxis_title="Business Unit",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)

    st.plotly_chart(fig_hourly, use_container_width=True)



    #Chart-5
    Storage_Cost_By_Month = df.groupby(by=["Branch"]).sum()[["Sales Value"]].round()
    # Storage_Cost_By_Month = Storage_Cost_By_Month .sort_values(by="Sales Value")

    fig_hourly_sales = px.bar(Storage_Cost_By_Month,
    x="Sales Value",
    y=Storage_Cost_By_Month.index,
    orientation="h",
    title="<b>Branch wise Sales</b>",
    text=(Storage_Cost_By_Month['Sales Value']),color_discrete_sequence=["#0083B8"])
    fig_hourly_sales.update_layout(height=650,width=1500,xaxis_title="Salary in Million",
    yaxis_title="Business Unit",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)
    #fig_hourly_sales.update_traces(marker_color="#fb7373")
    
    st.plotly_chart(fig_hourly_sales, use_container_width=True)

    st.markdown("")
    st.markdown("")

elif selected == "Delivery Analysis":


    col1, col2, col3,= st.columns(3)

    with col1:
       # st.markdown("Select Branches")
        selection_box1 = st.selectbox("Select Branches",
                                          options=df["Branch"].unique())
    with col2:
        selection_box2 = st.selectbox("Select Product",
                                          options=df["Product"].unique())
    with col3:
        selection_box3 = st.selectbox("Select Item Category",
                                          options=df["Item Category"].unique())
    
    df_se = df.query(
                "Branch == @selection_box1 ")
    
    st.markdown("")

    #Delivery Time
    delivery_time = df_se["Delivery Time"].mean()

    #Delivery Cost
    delivery_Cost = df_se["Delivery Cost"].mean()

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.markdown("<h4 style='text-align: center; color: black;'>Delivery Time</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #ff4b4c;'>"+str(round(delivery_time ))+"</h4>", unsafe_allow_html=True)

    with right_column:
        st.markdown("<h4 style='text-align: center; color: black;'>Delivery Cost</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #ff4b4c;'>"+str(round(delivery_Cost))+"</h4>", unsafe_allow_html=True)

    
    #Chart-1

    Storage_Cost_By_Month = df_se.groupby(["Product"])['Net Amount'].sum().reset_index()
    top10 = Storage_Cost_By_Month.nlargest(10, ['Net Amount'])

    fig = px.bar(top10, x='Product', y='Net Amount',orientation='v',title="<b>Top 10 Product & Values</b>"
    ,text=(top10['Net Amount']))
    fig.update_layout(xaxis_title="Product",
    yaxis_title="Sum of Net Amount",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)))
    fig.update_traces(marker_color="#3EC1CD")

    #Chart-2
    
    Storage_Cost_By_Month = df_se.groupby(["Product"])['Net Amount'].sum().reset_index()
    top10 = Storage_Cost_By_Month.nsmallest(10, ['Net Amount'])

    fig1 = px.bar(top10, x='Product', y='Net Amount',orientation='v',title="<b>Bottom 10 Product & Values</b>"
    ,text=(top10['Net Amount']))
    fig1.update_layout(xaxis_title="Product",
    yaxis_title="Sum of Net Amount",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)))
    fig1.update_traces(marker_color="#3EC1CD")

    left_column,right_column = st.columns(2)
    left_column.plotly_chart(fig,use_container_width=True)
    right_column.plotly_chart(fig1,use_container_width=True)

    #Chart3
    Storage_Cost_By_Month= df.groupby(by=["Item Category"]).mean()[["Delivery Cost"]].round(2).head(15).reset_index()
    fig = px.line(Storage_Cost_By_Month,x = 'Item Category',y='Delivery Cost',text=(Storage_Cost_By_Month['Delivery Cost']),
    title="<b>Average Delivery Cost by Category</b>"
    )
    fig.update_layout(xaxis_title="Item Category",
    yaxis_title="AVG Delivery Cost",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    xaxis=(dict(showgrid=False))
    )
    fig.update_traces(marker_color="#3EC1CD")


    st.plotly_chart(fig,use_container_width=True)


elif selected == "Sales Analysis":
    
    col1, col2, col3,col4,col5,col6= st.columns(6)

    with col1:
       # st.markdown("Select Branches")
        selection_box1 = st.selectbox("Select Branches",
                                          options=df["Branch"].unique())
    with col2:
        selection_box2 = st.selectbox("Select Channel",
                                          options=df["Channel"].unique())
    with col3:
        selection_box3 = st.selectbox("Select Item Category",
                                          options=df["Item Category"].unique())
    with col4:
        selection_box4 = st.selectbox("Select Product",
                                          options=df["Product"].unique())
    with col5:
        selection_box5 = st.selectbox("Select Brand",
                                          options=df["Brand"].unique())
    with col6:
        selection_box5 = st.selectbox("Select Purchase Date",
                                          options=df["Purchase_Date"].unique())

    
    #Chart-1
    Storage_Cost_By_Month = df.groupby(by=["Purchase_Date"])[["Profit"]].sum().reset_index().round()
    fig = px.line(Storage_Cost_By_Month,x = 'Purchase_Date',y='Profit',text=(Storage_Cost_By_Month['Profit']),
    title="<b>Profit Projection</b>"
    )
    fig.update_layout(xaxis_title="Item Category",
    yaxis_title="Profit",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    xaxis=(dict(showgrid=False))
    )
    fig.update_traces(marker_color="#3EC1CD")

    st.plotly_chart(fig,use_container_width=True)


    #Chart-2
    st.markdown("<h4 style='text-align: left; color: black;'>Store vs E-Comm</h4>", unsafe_allow_html=True)
    df_avg_bu=df.groupby(["Channel"],as_index=False)['Net Amount'].sum()
    fig = go.Figure(data=[go.Pie(labels=df_avg_bu['Channel'], values=df_avg_bu['Net Amount'],hole=.5)])         
    fig.update_layout(height=500,width=600)

    #Chart-3
    st.markdown("<h4 style='text-align: right; color: black;'>Returned Percentage</h4>", unsafe_allow_html=True)
    df_avg_bu=df.groupby(["Returned?"],as_index=False)['Returned?'].count()
    fig1 = go.Figure(data=[go.Pie(labels=df_avg_bu['Returned?'], values=df_avg_bu['Returned?'],hole=.5)])         
    fig1.update_layout(height=500,width=600)

    left_column,right_column = st.columns(2)

    left_column.plotly_chart(fig,use_container_width=True)
    right_column.plotly_chart(fig1,use_container_width=True)


    df_selection = df.groupby('Purchase_Date').agg({'Net Amount':'sum','Total Cost':'sum'}).reset_index().tail(15)
    fig_hourly_sales = px.bar(
    data_frame = df_selection,
    x = "Purchase_Date",
    y = ["Net Amount","Total Cost"],
    opacity = 0.9,
    orientation = "v",
    barmode = 'group',
    title='Weekly Trend',
    )
    fig_hourly_sales.update_layout(height=650,width=1500,xaxis_title="Purchase_date",
    yaxis_title="",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)

    st.plotly_chart(fig_hourly_sales,use_container_width=True)


