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
    buf = io.BytesIO()
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


#CREATE THE PLOTS----------------------------

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


#Function for graphic categorical ratings
def categorical_plot(data: list[dict]) -> str:
    """Creates the categorical rating plot (bar chart). View the frequency of categorical ratings

    Important Features:
        Skips rows when classification_ratings are null.
        Rating types are organized by severity

    """
    #Order and color of ratings
    ORDER = ["Poor", "Fair", "Good"]
    COLORS = ["#d73027", "#fff237", "#8aea6f"]

    #Counter that calculates the number of ratings in each category
    count_mapping = Counter(row.classification_ratings for row in data if row.classification_ratings is not None)

    #Calculate the categories (similar to ) 
    categories = [rate for rate in ORDER if rate in count_mapping] + \
                 [rate for rate in count_mapping if rate not in ORDER]
    
    counts = [count_mapping[rate] for rate in categories]

    #CHECK LITERALLY EVERYTHING BELOW LATER (To tired to check right now)
    graph_colors = COLORS[:len(categories)] if len(categories) <= 5 else ["#4C72B0"] * len(categories)

    view, axis = plt.subplots(figsize=(8, max(3, len(categories) * 0.8)))
    bars = axis.barh(categories, counts, color=graph_colors, edgecolor="white", height=0.55)

    for bar, count in zip(bars, counts):
        axis.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height() / 2,
                str(count), va="center", fontsize=10)
 
    axis.set_xlim(0, max(counts) * 1.15)
    default_style(view, axis,
                title="Mental Health Rating Distribution",
                xlabel="Number of Days",
                ylabel="Rating Category")
    return base_transfer(view)




#CHECK EVERYTHING BELOW (I DID NOT LOOK AT THIS)



def sleep_hours_plot(data: list[dict]) -> str:
    """
    Histogram of sleep_hours with a recommended-range band.
 
    Reads: row.sleep_hours (float | None)
    Skips rows where sleep_hours is None.
    """
    hours = [r.sleep_hours for r in data if r.sleep_hours is not None]
 
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(hours, bins=10, color="#5B8DB8", edgecolor="white", linewidth=0.7)
 
    # Highlight the recommended 7-9 hour range
    ax.axvspan(7, 9, alpha=0.15, color="#2ca02c", label="Recommended (7–9 hrs)")
    ax.legend(fontsize=9)
 
    default_style(fig, ax,
                title="Sleep Hours Distribution",
                xlabel="Hours of Sleep",
                ylabel="Number of Days")
    return base_transfer(fig)
 
 
def study_hours_plot(data: list[dict]) -> str:
    """
    Line chart with a shaded area for study_hours over time.
 
    Reads: row.study_hours (float | None), row.time (datetime)
    Skips rows where study_hours is None.
    """
    rows  = [r for r in data if r.study_hours is not None]
    dates = [r.time.strftime("%Y-%m-%d") for r in rows]
    hours = [r.study_hours for r in rows]
 
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(dates, hours, marker="s", linewidth=2, color="#E07B39", markersize=5)
    ax.fill_between(dates, hours, alpha=0.10, color="#E07B39")
 
    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=8)
    ax.set_ylim(0, max(hours) * 1.2 if hours else 10)
 
    default_style(fig, ax,
                title="Daily Study Hours Over Time",
                xlabel="Date",
                ylabel="Hours Studied")
    return base_transfer(fig)
 