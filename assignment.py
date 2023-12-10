import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def read_data(input_file):
    '''
    Parameters
    ----------
    input_file : input filename(.csv) fo read the data.

    Returns
    -------
    yearsdf : data with years as columns.
    countriesdf : data with years as columns.
    '''
    yearsdf = pd.read_csv(input_file, skiprows=3)
    countriesdf = yearsdf.transpose()
    return yearsdf, countriesdf


years = ["1980", "1990", "2000", "2010", "2015", "2020"]
countries = ["United Kingdom", "United States",
             "India", "Australia", "Canada", "Singapore"]
years_df, country_df = read_data("climate.csv")
indicator_code = "SP.POP.TOTL"
columns = list(years_df.columns)
df_temp = years_df
for year in years[:len(years) - 1]:
    columns.remove(year)
for i in range(len(df_temp)):
    if df_temp["Indicator Code"][i] != indicator_code:
        df_temp = df_temp.drop(i)
    else:
        continue
for i in range(len(columns)):
    df_temp = df_temp.drop(columns[i], axis=1)
summary = df_temp
print(summary.describe())


def heatmap_generator(data, countries, indicators):
    '''
    Generates a heatmap for specified countries and indicators based on input data.

    Parameters
    ----------
    data : pandas DataFrame
        Input data for cleaning the file.
    countries : list
        The required countries in the data.
    indicators : list
        The indicator codes for the specific features in the data.

    Returns
    -------
    None.
    '''
    indicator_data = {'Country': [], 'Attribute': [], 'Valuation': []}
    country_corr = ["United States", "United Kingdom", "India"]
    for i in range(len(data)):
        for j in range(len(indicators)):
            for k in range(len(country_corr)):
                if data["Country Name"][i] == country_corr[k] and data["Indicator Code"][i] == indicators[j]:
                    indicator_data['Valuation'].append(data["2010"][i])
                    indicator_data['Attribute'].append(
                        data["Indicator Name"][j])
                    indicator_data['Country'].append(country_corr[k])
    data_frame_indicator = pd.DataFrame(indicator_data)
    heatmap_data = data_frame_indicator.pivot_table(
        index='Country', columns=['Attribute'], values='Valuation', aggfunc='sum')
    correlation_matrix = heatmap_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='viridis')
    plt.title("Correlation Heatmap of Countries with Indicators as features")
    plt.show()


indicator_attributes = ["AG.LND.ARBL.ZS", "AG.LND.AGRI.ZS", "AG.LND.FRST.ZS",
                        "AG.LND.IRIG.AG.ZS", "EG.ELC.ACCS.ZS", "BX.KLT.DINV.WD.GD.ZS"]
# correlation heatmap plot
heatmap_generator(years_df, countries, indicator_attributes)


def line_plot(plot, indicators, source_data, years, countries, y, title):
    '''
    Extracts and processes data based on the specified indicator, source data, years, and countries.

    Parameters
    ----------
    indicators : str
        The indicator code for the specific feature in the data.
    source_data : pandas DataFrame
        The input data to be processed.
    years : list
        The required years to process the data.
    countries : list
        The required countries in the data.
    y : str
        Y axis title for the plot
    title: str
        title for the plot

    Returns
    -------
    final_result : list
        The output data with only the requested data from the given indicator.
    '''
    result_data = []
    data_frame_group = {}
    for year in years:
        for index, row in source_data.iterrows():
            for country in countries:
                if row["Indicator Code"] == indicators and row["Country Name"] == country:
                    result_data.append([row["Country Name"], row[year]])

    for key, value in result_data:
        if key not in data_frame_group:
            data_frame_group[key] = [value]
        else:
            data_frame_group[key].append(value)

    final_result = [[key, *values] for key, values in data_frame_group.items()]
    if plot == 1:
        plt.figure(figsize=(10, 6))
        for i in range(len(final_result)):
            country_name = final_result[i]
            data_points = final_result[i][1:]
            plt.plot(years, data_points, marker='*', linestyle='-.',
                     markersize=4, label=country_name[0])

        plt.xlabel('Year')
        plt.ylabel(y)
        plt.title(title)
        plt.legend()
        plt.show()
    else:
        return final_result


# Line chart plot
plotRain = line_plot(1, "AG.LND.PRCP.MM", years_df, years, countries, "Average precipitation in depth (mm per year)",
                     "Average precipitation of different countries in different years")
plotLand = line_plot(1, "AG.LND.AGRI.ZS", years_df, years, countries, "'Agricultural land (% of land area)'",
                     "'Total Agricultural land of different countries in different years'")


def bar_plot(data, years, y_axis, title):
    ''' 
    Parameters
    ----------
    data : Data for plotting the bar graph
    years : The axis labels and years data for multiple plots.
    y_axis : y axis label for the graph
    title : title for the plot

    Returns
    -------
    None.
    '''
    plt.figure(figsize=(9, 12))
    x_axis = np.arange(len(years))
    colors = ['#FF0000', '#00FF00', '#0000FF',
              '#FFFF00', '#800080', '#FFA500', '#008080']

    for i in range(len(data)):
        plt.barh(x_axis + i*0.1, data[i][1:], 0.1,
                 color=colors[i], label=data[i][0])

    plt.yticks(x_axis, years)
    plt.xlabel('Year')
    plt.title(title)
    plt.ylabel(y_axis)
    plt.legend()
    plt.show()


years_barplot = ["1990", "2000", "2005", "2010", "2015", "2020"]
data_bar_chart = line_plot(
    0, "AG.YLD.CREL.KG", years_df, years_barplot, countries, "", "")
# Bar chart plot
bar_plot(data_bar_chart, years_barplot, "Cereal yield (kg per hectare)",
         "Cereal yield of different countries")


def pie_plot(data, labels, title):
    '''
    Parameters
    ----------
    data : List of data for each category.
    labels : List of labels for each country name.
    title : Title of the pie chart.

    Returns
    -------
    None.
    '''
    plt.figure(figsize=(4, 4))
    wedges, texts, autotexts = plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#800080', '#008080'],
                                       textprops=dict(color="w"))
    plt.legend(wedges, labels, title="Categories",
               loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=10, weight="bold", color="black", rotation=45)
    plt.title(title)
    plt.show()


data_bar_graph = line_plot(
    0, "AG.LND.AGRI.K2", years_df, years_barplot, countries, "", "")
for i in range(0, len(countries)):
    years_pie = years
    data_pie_chart = [data_bar_graph[0][1:][i], data_bar_graph[1][1:][i], data_bar_graph[2]
                      [1:][i], data_bar_graph[3][1:][i], data_bar_graph[4][1:][i], data_bar_graph[5][1:][i]]
    countries_data = []
    for j in range(0, len(data_bar_graph)):
        countries_data.append(data_bar_graph[j][0])
    title_pie_chart = 'Agricultural land (sq. km) in ' + str(years_pie[i])
    # Pie chart plot
    pie_plot(data_pie_chart, countries_data, title_pie_chart)


def table(summary):
    '''
    Parameters
    ----------
    summary : List of data for each category.


    Returns
    -------
    table : dataframe for the table.
    '''
    table_plot = summary.head()
    data_table = table_plot.values.tolist()
    data = {
        years[0]: data_table[0],
        years[1]: data_table[1],
        years[2]: data_table[2],
        years[3]: data_table[3],
        years[4]: data_table[4]
    }
    countries_table = ["United Kingdom",
                       "United States", "India", "Australia", "Canada"]
    # create Table
    table = pd.DataFrame(data, index=countries_table)
    return table


print(table(summary))
