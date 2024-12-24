import pandas as pd
import plotly.express as px
import streamlit as st
import difflib

#emojis:https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

sales_df=pd.read_csv('sales.csv')



#add 'hour' column to dataframe
sales_df["Time"] = sales_df["Time"] + ":00"
sales_df["hour"]=pd.to_datetime(sales_df["Time"],format="%H:%M:%S").dt.hour



st.sidebar.header("Please Filter Here:")
city=st.sidebar.multiselect(
    "Select the City:",
    options=sales_df["City"].unique(),
    default=sales_df["City"].unique()
    
)

customer_type=st.sidebar.multiselect(
      "Select the Customer Type:",
      options=sales_df["Customer type"].unique(),
      default=sales_df["Customer type"].unique()
        
)

gender=st.sidebar.multiselect(
      "Select the Gender:",
      options=sales_df["Gender"].unique(),
      default=sales_df["Gender"].unique()
        
)


df_selection = sales_df.query(
    "`City` in @city and `Customer type` in @customer_type and `Gender` in @gender"
)

#Mainpage
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#Top KPI's
total_sales=int(df_selection["Total"].sum())
average_rating=round(df_selection["Rating"].mean(),1)
star_rating=":star:" * int(round(average_rating,0))
average_sale_by_transaction=round(df_selection["Total"].mean(),2)

left_column, middle_column, right_column=st.columns(3)
with left_column:
    st.subheader("total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $  {average_sale_by_transaction}")

st.markdown("---")


#Sales by product line(bar chart)
sales_by_product_line=(
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")

)
fig_product_sales=px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#008388"]*len(sales_by_product_line),
    template="plotly_white"
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


#sales by hour[bar chart]
sales_by_hour=df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales=px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#008388"]*len(sales_by_hour),
    template="plotly_white"
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column,right_column=st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales,use_container_width=True)

#hide streamlit style
import streamlit as st

# Apply custom CSS to hide Streamlit's style elements
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;} /* Hides the hamburger menu */
        footer {visibility: hidden;}   /* Hides the footer */
        header {visibility: hidden;}   /* Hides the header */
    </style>
"""

# Inject the CSS into the app
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

