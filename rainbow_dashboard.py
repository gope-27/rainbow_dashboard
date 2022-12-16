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
selected = option_menu("Rainbow Dashboard", ["Sales Analysis","Store Analysis", "Delivery Analysis","Customer Analysis" ],#, "Customer Analysis", "Inventory Analysis"
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


def get_data_from_csv():
    df = pd.read_csv("Rainbow_Final_Dataset.csv")
    df_inn = pd.read_csv("Innovation Customer table.csv")
    df1 =(df['Profit']/df['Net Amount'] * 100).round()
    gross_margin = df1
    df['gross_margin'] = gross_margin
    index_list = list(range(2698, 2814))
    df.drop(df.index[index_list], inplace =True)
    return df,df_inn


df ,df_inn= get_data_from_csv()

if selected == "Store Analysis": #for Selecting the field
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
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
    fig_hourly_sales.update_layout(xaxis_title="Branch",
    yaxis_title="SUM of Net Amount and Total Cost",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)
    #fig_hourly_sales.update_traces(marker_color="#fb7373")

    st.plotly_chart(fig_hourly_sales, use_container_width=True)

    # #chart-4
    df_se = df.groupby(['Branch','Channel']).agg({'Order number':'count'}).reset_index()
  
    fig_hourly_sales = px.bar(
    data_frame = df_se,
    x = "Branch",
    y = ["Order number"],
    color="Channel",    
    barmode = 'stack',
    title='<b>Branch Performance through Channel<b>'
        )

    fig_hourly_sales.update_layout(xaxis_title="Branch",
    yaxis_title="Order Count",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)

    st.plotly_chart(fig_hourly_sales, use_container_width=True)

    
    #Chart - 5
    df_se = df.groupby(['Purchase_Date']).agg({'Net Amount':'sum','Cost':'sum'}).reset_index().tail(10)
    fig_hourly_sales = px.bar(
    data_frame = df_se,
    x = "Purchase_Date",
    y = ["Net Amount","Cost"], 
    orientation = "v",
    barmode = 'group',
    title='<b>Weekly Trend<b>',
    # color_discrete_sequence=["#0083B8"]
        )
    fig_hourly_sales.update_layout(xaxis_title="Purchase Date",
    yaxis_title="SUM of Net Amount and Cost",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)

    st.plotly_chart(fig_hourly_sales, use_container_width=True)

    #Chart-5
    df_se = df.groupby(['Purchase_Date']).agg({'Net Amount':'sum','Cost':'sum'}).reset_index()
    fig_hourly_sales = px.bar(
    data_frame = df_se,
    x = "Purchase_Date",
    y = ["Net Amount","Cost"],
            
    orientation = "v",
    barmode = 'group',
    title='<b>Monthly Trend<b>',
        # color_discrete_sequence=["#0083B8"]
        )
    fig_hourly_sales.update_layout(xaxis_title="Purchase Date",
    yaxis_title="Business Unit",plot_bgcolor="rgba(0,0,0,0)")   
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)

    st.plotly_chart(fig_hourly_sales, use_container_width=True)

    #Chart-6
    Storage_Cost_By_Month = df.groupby(by=["Branch"]).sum()[["Sales Value"]].round()
    # Storage_Cost_By_Month = Storage_Cost_By_Month .sort_values(by="Sales Value")

    fig_hourly_sales = px.bar(Storage_Cost_By_Month,
    x="Sales Value",
    y=Storage_Cost_By_Month.index,
    orientation="h",
    title="<b>Branch wise Sales</b>",
    text=(Storage_Cost_By_Month['Sales Value']),color_discrete_sequence=["#0083B8"])
    fig_hourly_sales.update_layout(height=650,width=1500,xaxis_title="Branch",
    yaxis_title="SUM Of Sales Values",plot_bgcolor="rgba(0,0,0,0)")
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
    
    # df_se = df.query(
    #             "Branch == @selection_box1 ")

    df_se = df.query(
    "Branch == @selection_box1 "
)
    
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
    #fig1.update_traces(marker_color="#3EC1CD")

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
    #fig.update_traces(marker_color="#3EC1CD")


    st.plotly_chart(fig,use_container_width=True)

    #Chart-4
    df1 = df.groupby(['Delivery Agent']).agg({'Delivery Time':'mean'}).reset_index().round(2)
    data0 = go.Scatter(x = df1['Delivery Agent'],
                    y = df1['Delivery Time'],
                    name = 'AVG Delivery Time',
                    text =  df1['Delivery Time'],
                    # textposition = 'top left',
                    mode = 'markers + lines')


    df2 = df.groupby(['Delivery Agent']).agg({'Delivery Cost':'mean'}).reset_index().round(2)
    data1 = go.Bar(y = df2['Delivery Cost'],
                    x = df2['Delivery Agent'],
                    name = 'AVG Delivery Cost',
                    text = df2['Delivery Cost'],
                    textposition = 'outside',)

    data = [data0,data1]
    layout = go.Layout(title = "Average Delivery Time & Cost by Delivery Partners",barmode = 'stack')
    figure = go.Figure(data = data,layout = layout)
    figure.update_layout(xaxis_title="Product",
    yaxis_title="Sum of Net Amount",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)))
    #figure.update_traces(marker_color="#3EC1CD")

    st.plotly_chart(figure,use_container_width=True)


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

    st.markdown("")
    df_sel = df.query(
                "Branch == @selection_box1 ")

    
    #Chart-1
    Storage_Cost_By_Month = df_sel.groupby(by=["Purchase_Date"])[["Profit"]].sum().reset_index().round()
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

    df_selection = df.groupby('Purchase_Date').agg({'Net Amount':'sum','Total Cost':'sum'}).reset_index().tail(7)
    fig_hourly_sales = px.bar(
    data_frame = df_selection,
    x = "Purchase_Date",
    y = ["Net Amount","Total Cost"],
    opacity = 0.9,
    orientation = "v",
    barmode = 'group',  
    title='Weekly Trend'
    )
    fig_hourly_sales.update_layout(height=650,width=1500,xaxis_title="Purchase_date",
    yaxis_title="",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)

    st.plotly_chart(fig_hourly_sales,use_container_width=True)

    #Chart-4
    df_se = df.groupby(['Branch']).agg({'Net Amount':'sum','Cost':'sum'}).reset_index()
    top10 = df_se.nlargest(7,'Net Amount')
    fig_hourly_sales = px.bar(
    data_frame = top10,
    x = "Branch",
    y = ["Net Amount","Cost"],
            
    orientation = "v",
    barmode = 'stack',
    title='<b>Weekly Trend<b>',
    # color_discrete_sequence=["#0083B8"]
        )
    fig_hourly_sales.update_layout(xaxis_title="Salary in Million",
    yaxis_title="Business Unit",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)

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
    

    #chart-4
    df_se = df.groupby(['Branch']).agg({'Net Amount':'sum','Cost':'sum'}).reset_index()
    top10 = df_se.nlargest(7,'Net Amount')
    fig_hourly_sales = px.bar(
    data_frame = top10,
    x = "Branch",
    y = ["Net Amount","Cost"],
            
    orientation = "v",
    barmode = 'stack',
    title='<b>Top Performing Branches<b>',
    # color_discrete_sequence=["#0083B8"]
        )
    fig_hourly_sales.update_layout(xaxis_title="Branch",
    yaxis_title="Business Unit",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)

    st.plotly_chart(fig_hourly_sales,use_container_width=True)


    #Char-4
    df1 = df.groupby(['Branch']).agg({'Net Amount':'sum','Cost':'sum','Profit':'sum','gross_margin':'mean','CustID':'count'}).reset_index().round()

    st.table(df1)

if selected == "Customer Analysis":
    Storage_Cost_By_Month = df.groupby(['Customer name']).agg({'Profit':'sum'}).reset_index().round()
    top10 = Storage_Cost_By_Month.nlargest(10, ['Profit'])
    fig_hourly_sales = px.bar(
    data_frame = top10,
    x = "Customer name",
    y = "Profit",
    text = "Profit",
    orientation = "v",
    #barmode = 'group',
    title='<b>Most Valuable Customers<b>',
    # color_discrete_sequence=["#0083B8"]
        )
    fig_hourly_sales.update_layout(xaxis_title="Customer name",
    yaxis_title="Business Unit",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)

    #Chart-2
    Storage = df.groupby(['Customer name']).agg({'Profit':'sum'}).reset_index().round()
    top10 = Storage.nlargest(10, ['Profit'])
    fig = px.bar(
    data_frame = top10,
    x = "Customer name",
    y = "Profit",
    text = "Profit",
    orientation = "v",
    #barmode = 'group',
    title='<b>Regular Customers<b>',
    # color_discrete_sequence=["#0083B8"]
        )
    fig.update_layout(xaxis_title="Customer name",
    yaxis_title="Business Unit",plot_bgcolor="rgba(0,0,0,0)")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    col1,col2 = st.columns(2)

    col1.plotly_chart(fig_hourly_sales,use_container_width=True)
    col2.plotly_chart(fig,use_container_width=True)

    #chart-3
   # df_inn = pd.read_csv("Innovation Customer table.csv")
    Storage_Cost_By_Month = df_inn.groupby(['Customer name']).agg({'Total Purchase Till Date in Rupees':'sum'}).reset_index().round()
    top10 = Storage_Cost_By_Month.nlargest(10, ['Total Purchase Till Date in Rupees'])
    fig_hourly_sales = px.line(
    data_frame = top10,
    x = "Customer name",
    y = "Total Purchase Till Date in Rupees",
    text = "Total Purchase Till Date in Rupees",
    orientation = "v",
    #barmode = 'group',
    title='<b>Top Customers by totl purchase made till date<b>',
    # color_discrete_sequence=["#0083B8"]
        )
    fig_hourly_sales.update_layout(xaxis_title="Customer name",
    yaxis_title="",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourly_sales.update_xaxes(showgrid=False)
    fig_hourly_sales.update_yaxes(showgrid=False)

    #Chart-4
    dd = df.groupby(['Customer Regularity']).agg({'CustID':'count'}).reset_index()
    fig_hourl = px.bar(
    data_frame = dd,
    x = "Customer Regularity",
    y = "CustID",
    text = "CustID",
    orientation = "v",
    #barmode = 'group',
    title='<b>Customer Regularity till date<b>',
    # color_discrete_sequence=["#0083B8"]
        )
    fig_hourl.update_layout(xaxis_title="Customer name",
    yaxis_title="",plot_bgcolor="rgba(0,0,0,0)")
    fig_hourl.update_xaxes(showgrid=False)
    fig_hourl.update_yaxes(showgrid=False)


    #Chart-5
    Storage_Cost_By_Month = df_inn.groupby(['City']).agg({'Average Ticket Size':'mean'}).reset_index().round()
    #Storage_Cost_By_Month = df1.groupby(['City']).agg({'Average Ticket Size':'mean'}).reset_index().round()
    top10 = Storage_Cost_By_Month.nlargest(10, ['Average Ticket Size'])
    fig = px.line(
    data_frame = top10,
    x = "City",
    y = "Average Ticket Size",
    text = "Average Ticket Size",
    orientation = "v",
    #barmode = 'group',
    title='<b>Average Ticket Size by city<b>',
    # color_discrete_sequence=["#0083B8"]
        )
    fig.update_layout(xaxis_title="Customer name",
    yaxis_title="",plot_bgcolor="rgba(0,0,0,0)")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    col1,col2,col3 = st.columns(3)

    col1.plotly_chart(fig_hourly_sales,use_container_width=True)
    col2.plotly_chart(fig_hourl,use_container_width=True)
    col3.plotly_chart(fig,use_container_width=True)

    #Char-4
    tab = df_inn.groupby(['City']).agg({'Age':'mean','Total Purchase Till Date in Rupees':'mean','Total Returns Till Date in Rupees':'mean'}).reset_index().round()


    st.table(tab)

