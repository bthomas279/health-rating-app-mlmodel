from __future__ import annotations #Allows string-based type hints 
#This will hold a class that contains the code to be operated for each specific plot

#Imports
import base64
import io
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


#Function for transfering plot to base64
def base_transfer(fig: plt.Figure) -> str:
    """Serialize matplotlib figures to base64"""
    buf = io.BytesIO
    #Save plot as png
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    #Encode plot
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    #Close figure
    plt.close(fig)
    
    return encoded
    
#Function to give default styling
def default_style(fig: plt.Figure, axis: plt.Axes, title: str, xlabel: str, ylabel: str):
    """Create defult styling for all plots"""
    axis.set_title(title, fontsize=15, fontweight = "bold", pad=14) #title
    axis.set_xlabel(xlabel, fontsize=11) #x axis
    axis.set_ylabel(ylabel, fontsize=11) #y axis
    axis.spines[["top", "right"]].set_visible(False) 
    axis.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    axis.grid(axis="y", linestyle="--", alpha=0.4) #grid 
    fig.tight_layout #layout


#CREATE THE PLOTS 

#Function for graphic numerical ratings
def numerical_plot(data: list[dict]) -> str:
    """Creates the numerical rating plot (line plot). View regression ratings over time.

    Important Features:
        Skips rows when regression_ratings are null.

    """
    #Grab non-null regression rows
    rows = [row for row in data if row.regression_ratings is not None]
    #Grab times
    dates = [row.time.strftime("%Y-%m-%d") for row in rows]
    #Grab ratings
    ratings = [row.regression_ratings for row in rows]

    #Determine plot size and characteristics
    view, axis = plt.subplots(figsize=(9,4))
    axis.plot(dates, ratings, marker="o", linewidth=2, color="#4C72B0", markersize=5)

    axis.fill_between(dates, ratings, alpha=0.08, color="#4C72B0")

    #For the x and y axis
    axis.set_xticks(range(len(dates)))
    axis.set_xticklabels(dates, rotation=45, ha="right", fontsize=8)
    axis.set_ylim(0, 1) #Once I change the rating structure, make it 0 - 10


    #Insert default style into plot
    default_style(view, axis,title= "Mental Health Ratings (Numerical)",
                  xlabel= "Date",
                  ylabel= "Rating (0 - 1)") #Change rating label later
    #Return plot
    return base_transfer(view)



def numerical_plot(data: list[dict]) -> str:
    """Creates the categorical rating plot (bar chart). View the frequency of categorical ratings

    Important Features:
        Skips rows when classification_ratings are null.
        Rating types are organized by severity

    """
    #Order and color of ratings
    ORDER = ["Poor", "Fair", "Good"]
    COLORS = ["#d73027", "#fff237", "#8aea6f"]

    #Counter that calculates the number of ratings in each category






    