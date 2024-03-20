from taipy.gui import Gui
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb

path = 'data/supermarkt_sales.xlsx'
paths = []
dfs = []

# dataset standart
def import_data(path):
    data = pd.read_excel(path)
    return data

#def file_names(state):
    


# import data cliente
def import_file(state):
    paths = list(state.path)
    for p in paths:
        df = pd.read_excel(p)
        dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    #print(combined_df.head())
    print(combined_df.shape)

# filter city table
def filter_column(data, cities):
    df = data[data['City'].isin(cities)]
    return df

# creator of pie plot by groupby
def create_pie_figure(data, group_by:str):
    grouped_data = data.groupby(group_by)['Total'].sum().reset_index()
    grouped_data['Total'] = grouped_data['Total'].round(2)
    fig = px.pie(grouped_data, names= group_by, values='Total', title=f"Sales Performance by {group_by}", hole=0.3)
    return fig

# creator of bar plot by groupby
def create_bar_figure(data, group_by:str):
    sales_over_time = data.groupby(group_by)['Total'].sum().reset_index()
    fig = px.bar(sales_over_time, x=group_by, y='Total', title="Salaes Trends Over Time", color='Total')
    return fig

# creator of percent plot by groupby
def create_perc_fig(df, group_column):
    df = df.groupby(['Date', group_column])['Total'].sum().unstack(fill_value=0)
    df = df.div(df.sum(axis=1), axis=0).reset_index().melt(id_vars='Date', var_name=group_column, value_name='Percentage')
    df['Percentage'] = (df.loc[:, 'Percentage'].round(3) * 100)
    
    # Create and return the plot
    fig = px.bar(df, x='Date', y='Percentage', color=group_column, title=f"Evolution of Sales by {group_column} over Time", labels={'Percentage': '% of Total'}, text_auto=True)
    return fig

# change on selector variables
def on_selector(state):
    state.data = import_data(path)
    filtered_data = data.loc[
    state.data['City'].isin(state.city)
    ]

    state.data = filter_column(data,state.city)

    state.fig_product_line_perc = create_perc_fig(filtered_data, 'Product_line')
    state.fig_city_perc = create_perc_fig(filtered_data, 'City')
    state.fig_gender_perc = create_perc_fig(filtered_data, 'Gender')
    state.fig_customer_type_perc = create_perc_fig(filtered_data, 'Customer_type')
    
# main
data = import_data(path)

pie_fig_city = create_pie_figure(data, 'City')
pie_fig_gender = create_pie_figure(data, 'Gender')

fig_time = create_bar_figure(data, 'Date')

city = ['Naypyitaw', 'Yangon', 'Mandalay']
gender = ['Female', 'Male']

filtered_data = data.loc[
    data['City'].isin(city)
]

fig_product_line_perc = create_perc_fig(filtered_data, 'Product_line')
fig_city_perc = create_perc_fig(filtered_data, 'City')
fig_gender_perc = create_perc_fig(filtered_data, 'Gender')
fig_customer_type_perc = create_perc_fig(filtered_data, 'Customer_type')

with tgb.Page() as page:
    tgb.text("Sales Insights", class_name="h1")

    with tgb.layout("1"):

        tgb.file_selector("{path}", label="Select File", on_action=import_file, multiple=True, extensions=".csv,.xlsx", drop_message="Drop Message")


        with tgb.layout("1 1 1"):
            with tgb.part():
                tgb.text("Total Sales", class_name="h2")
                tgb.text("{int(data['Total'].sum())}", class_name= "h3")

            with tgb.part():
                tgb.text("Average Sales", class_name="h2")
                tgb.text("{int(data['Total'].mean())}", class_name="h3")

            with tgb.part():
                tgb.text("Mean Rating", class_name="h2")
                tgb.text("{int(data['Rating'].mean())}", class_name="h3")

        with tgb.layout("1 1"):
            with tgb.part():
                tgb.chart(figure="{pie_fig_city}")
            with tgb.part():
                tgb.chart(figure="{pie_fig_gender}")
        
        
        tgb.chart(figure="{fig_time}")
            
        tgb.text("Analysis", class_name="h2")

        tgb.selector(value="{city}", lov=['Naypyitaw', 'Yangon', 'Mandalay'],
                     dropdown=True,
                     multiple=True,
                     label="Select cities",
                     class_name="full_width",
                     on_change=on_selector)

        with tgb.layout("1 1"):
            tgb.chart(figure="{fig_product_line_perc}")
            tgb.chart(figure="{fig_city_perc}")
            tgb.chart(figure="{fig_gender_perc}")
            tgb.chart(figure="{fig_customer_type_perc}")

            #with tgb.part():

    
        tgb.table("{data}")


if __name__=="__main__":
    gui = Gui(page)
    gui.run(title="Sales", port=2452)