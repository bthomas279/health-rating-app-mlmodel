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
    """Creates the numerical rating plot. Should be expecting

    """







