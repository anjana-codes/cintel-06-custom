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
shinyswatch.theme.superhero()

#Reactive Aspects 
# Reactive calculation to filter data based on selected species and islands
@reactive.calc
def filtered_data():
    return penguins_df[
        (penguins_df["species"].isin(input.selected_species_list())) &
        (penguins_df["island"].isin(input.selected_island_list()))
    ]
#UI Page Inputs
# names the page
ui.page_opts(title="Penguins Data - Anjana", fillable=True)

#UI Sidebar Components
# creates sidebar for user interaction
with ui.sidebar(position = "right", open="open"):
    ui.h2("Sidebar")
    
    # Creates a dropdown input to choose a column 
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    ui.input_selectize(
        "selected_gender",
       "Select Sex",
        ["male", "female"],
    )


    # Adds a horizontal rule to the sidebar
    ui.hr()
    
    # Creates a checkbox group input
    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True,
    )

    # Creates a checkbox group input for islands
    ui.input_checkbox_group(
        "selected_island_list",
        "Islands",
        penguins_df["island"].unique().tolist(),
        selected=penguins_df["island"].unique().tolist(),
        inline=True,
    )

  # Adds a hyperlink to GitHub Repo
    ui.a(
        "Anjana's GitHub",
         href="https://github.com/anjana-codes/cintel-02-data",
         target="_blank",
         )

    ui.a(
        "Dashboard Template",
         href="https://shiny.posit.co/py/templates/dashboard/",
         target="_blank",
         )


#Choose at least one input that the user can interact with to filter the data set

#UI Main Content
# Accordion component for the histograms        

    with ui.accordion_panel("Scatterplot"):
        with ui.card():
            ui.card_header("Plotly Scatterplot: Species")
            @render_plotly
            def plotly_scatterplot():
                return px.scatter(filtered_data(),
                                    x="bill_length_mm",
                                    y="bill_depth_mm",
                                    color="species",
                                  color_discrete_map={
                     'Adelie': 'yellow',
                     'Chinstrap': 'brown',
                     'Gentoo': 'green'}
                  )
#Everything not in the sidebar is the main content.
#Will you use a template?
#Will you use layout columns?
#Will you use navigation or accordion components?
#Define some output text. Will it be in a card? A value box? 
#Define an output table or grid to show your filtered data set
#Define an  output widget or chart (e.g., a Plotly Express chart) to show the filtered data graphically
 
