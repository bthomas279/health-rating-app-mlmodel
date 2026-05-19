from __future__ import annotations #Allows string-based type hints 
#This will hold a class that contains the code to be operated for each specific plot

#Imports
import base64
import io
from collections import Counter,  defaultdict
from typing import TYPE_CHECKING
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#Function to find the average
def average(values: list[float]) -> float:
    """Returns the mean of a list of numeric values. In this case, it is used
    to find the average value of a specific date.
    """
    return sum(values) / len(values)

#Function to group rows 
def date_grouping(rows: list, field: str) -> tuple[list[str], list[float]]:
    """Function that groups rows that share the same date and finds the average of
    those groups. (Doesn't effect groups with one value).

    Args:
        Rows and fields of inputs.

    Returns:
        dates (list): A sorted list of unique date strings ("YYYY_MM-DD")
        averages: the average values for each date
    """
    #defaultdict() automaticaly creates an empty lsit for any key not seen before (don't need to check beforhand)
    #bucket each value into groups based on dates
    bucket: dict[str, list[float]] = defaultdict(list)
    
    for row in rows: 
        #Convert datetimes
        str_date = row.time.strftime("%Y-%m-%d")
        #Get the field by names
        value = getattr(row, field)
        bucket[str_date].append(value)

    #Sort the dates chronologically (chart reads from left to right)
    sorted_dates = sorted(bucket.keys())

    #Compute the average of all values for each specific date
    date_averages = [average(bucket[date]) for date in sorted_dates]
    
    return sorted_dates, date_averages



#Function for transfering plot to base64
def base_transfer(fig: plt.Figure) -> str:
    """Coverts matplotlib figures to base64 encoded PNG strings. This allows it
    to be enbedded into JSON and rendered in HTML.
    """
    #Render BytesIO() as a buffer (like a file)
    buf = io.BytesIO()
    #Save plot as png (Write PNG bytes into buffer)
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    #Rewrite the buffer to the start (allows it to be viewed)
    buf.seek(0)

    #Encode plot (Convert raw bytes to Base64 bytes)
    #Decode converts Base64 bytes to a plain Python string
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    #Close figure (frees memory)
    plt.close(fig)
    
    return encoded
    
#Function to give default styling for every chart
def default_style(fig: plt.Figure, axis: plt.Axes, title: str, xlabel: str, ylabel: str):
    """Create defult styling for all plots. Allows for each chart to look similar and cohesive.
    
    Includes:
        Bold title
        Axis labels
        Removes the top and right border lines 
        Adds subite horizontial grid lines
    """
    axis.set_title(title, fontsize=15, fontweight = "bold", pad=14) #title
    axis.set_xlabel(xlabel, fontsize=11) #x axis
    axis.set_ylabel(ylabel, fontsize=11) #y axis
    #Hide the top/right chart border
    axis.spines[["top", "right"]].set_visible(False) 

    axis.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    axis.grid(axis="y", linestyle="--", alpha=0.4) #grid  structure
    fig.tight_layout #Revents labels from being cut off at the edges


#CREATE THE PLOTS----------------------------

#Function for graphic numerical ratings
def numerical_plot(data: list[dict]) -> str:
    """Creates the numerical rating plot (line plot). View regression ratings over time.

    Important Features:
        Skips rows when regression_ratings are null.
        If the same day appears multiple times, the rates are averaged a single values
        to display.
    """
    #Only grabs all non-null regression rows
    rows = [row for row in data if row.regression_ratings is not None]
    #Grab days, times and find the averages
    dates, ratings = date_grouping(rows, "regression_ratings")

    #Determine plot size and characteristics
    view, axis = plt.subplots(figsize=(9,4))
    #Create and plot the line connecting each average point by day
    axis.plot(dates, ratings, marker="o", linewidth=2, color="#4C72B0", markersize=5)

    #Crete a shaded area under the line plotted 
    axis.fill_between(dates, ratings, alpha=0.08, color="#4C72B0")

    #Set the x-axis tick positions 
    axis.set_xticks(range(len(dates)))

    #Edit x labels (includes rotation)
    axis.set_xticklabels(dates, rotation=45, ha="right", fontsize=8)
    
    #Set Y axis range
    axis.set_ylim(0, 1) #Once I change the rating structure, make it 0 - 10


    #Insert default style into plot
    default_style(view, axis, title= "Mental Health Ratings (Numerical)",
                  xlabel= "Date",
                  ylabel= "Average Ratings (0 - 1)") #Change rating label later
    #Return plot
    return base_transfer(view)


#Function for graphic categorical ratings
def categorical_plot(data: list[dict]) -> str:
    """Creates the categorical rating plot (bar chart). View the frequency of categorical ratings occuring over time.

    Important Features:
        Skips rows when classification_ratings are null.
        Rating types are organized by severity
        Chart 

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
 