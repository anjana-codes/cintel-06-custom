#Imports
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns
from shiny import reactive, render, req
import shinyswatch
from faicons import icon_svg

# Theme
shinyswatch.theme.darkly()

# Reactive calculation to filter data based on selected species and islands
@reactive.calc
def filtered_data():
    return penguins_df[
        (penguins_df["species"].isin(input.selected_species_list())) &
        (penguins_df["island"].isin(input.selected_island_list()))
    ]

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# names the page
#ui.page_opts(title="Penguins Data - Anjana", fillable=True)

# creates sidebar for user interaction
with ui.sidebar(position = "right", open="open"):
    ui.h2("Sidebar")
    
    # Creates a dropdown input to choose a column 
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"] 
    )

  
    # Adds a horizontal rule to the sidebar
    ui.hr()
    
    # Creates a checkbox group input
    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )

    # Creates a checkbox group input for islands
    ui.input_checkbox_group(
        "selected_island_list",
        "Islands",
        penguins_df["island"].unique().tolist(),
        selected=penguins_df["island"].unique().tolist(),
        inline=False,
    )

  # Adds a hyperlink 
    ui.a(
        "Anjana's GitHub",
         href="https://github.com/anjana-codes/cintel-06-custom",
         target="_blank",
         )
    ui.a(
        "Penguins Dataset",
         href="https://github.com/mcnakhaee/palmerpenguins/blob/master/palmerpenguins/data/penguins.csv",
         target="_blank",
         )

    ui.a(
        "Dashboard Template",
         href="https://shiny.posit.co/py/templates/dashboard/",
         target="_blank",
         )
    
 #The main section with according, cards, value boxes, and space for grids and charts
with ui.accordion():
    with ui.accordion_panel("Penguins Dashboard"):
        with ui.layout_columns():
            with ui.value_box(showcase=icon_svg("snowman"),width="50px", theme="bg-gradient-orange-red"
                             ):
                "Number of  Penguins"
                @render.text
                def display_penguin_count():
                    df = filtered_data()
                    return f"{len(df)}"

            with ui.value_box(showcase=icon_svg("ruler-horizontal"),width="50px", theme="bg-gradient-blue-purple"
                             ):
                "Average Bill Length"
                @render.text
                def average_bill_length():
                    df = filtered_data()
                    return f"{df['bill_length_mm'].mean():.2f} mm" if not df.empty else "N/A"

            with ui.value_box(showcase=icon_svg("ruler-vertical"),width="50px", theme="bg-gradient-blue-purple"
                             ):
                "Average Bill Depth"
                @render.text
                def average_bill_depth():
                    df = filtered_data()
                    return f"{df['bill_depth_mm'].mean():.2f} mm" if not df.empty else "N/A"
                

# Creates a DataGrid showing all data (outcome with layout_column)
with ui.layout_columns():        
    with ui.card(full_screen=True):
        ui.h2("Penguin Data")

        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(filtered_data(), filters=True) 

# Creates a Plotly Scatterplot showing all species and islands

    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                filtered_data(),
                title="Plotly Scatterplot",
                  x="bill_depth_mm",
                y="bill_length_mm",
                color="species",
                color_discrete_map={
                     'Adelie': 'orange',
                     'Chinstrap': 'purple',
                     'Gentoo': 'green'},
              
            )

