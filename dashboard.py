import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from io import BytesIO

# Function to convert graphs to PNG and download
def download_plot(fig, filename="plot.png"):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Dashboard function with graphs
def show_dashboard():
    st.markdown("<h1 style='text-align:center;'>Dashboard</h1>", unsafe_allow_html=True)

    # Data for the graphs
    x = np.linspace(0, 10, 100)
    bar_x = np.array([1, 2, 3, 4, 5])
    scatter_x = np.random.rand(100)
    scatter_y = np.random.rand(100)

    # Sidebar graph options
    graph_options = st.sidebar.radio(
        "Choose a graph",
        options=("Line Chart", "Bar Chart", "Horizontal Bar Chart", "Scatter Plot")
    )

    # Use a container
    with st.container():
        # Line Chart
        if graph_options == "Line Chart":
            st.markdown("<h2 style='text-align:center;'>Line Chart</h2>", unsafe_allow_html=True)
            sin_color_option = st.sidebar.selectbox("Choose a color for sin(x)", ("blue", "green", "red"))
            sin_line_style = st.sidebar.selectbox("Choose a line style for sin(x)", ("-", "--", "-.", ":"))
            cos_color_option = st.sidebar.selectbox("Choose a color for cos(x)", ("blue", "green", "red"))
            cos_line_style = st.sidebar.selectbox("Choose a line style for cos(x)", ("-", "--", "-.", ":"))
            
            color_mapping = {"blue": "blue", "green": "green", "red": "red"}
            
            fig_line_chart = plt.figure()
            plt.plot(x, np.sin(x), color=color_mapping[sin_color_option], linestyle=sin_line_style, label='sin(x)')
            plt.plot(x, np.cos(x), color=color_mapping[cos_color_option], linestyle=cos_line_style, label='cos(x)')
            plt.legend()
            st.pyplot(fig_line_chart)

            # Add a download button for the line chart
            buf_line_chart = download_plot(fig_line_chart)
            st.download_button("Download Line Chart as PNG", buf_line_chart, "line_chart.png", "image/png")

        # Bar Chart
        elif graph_options == "Bar Chart":
            st.markdown("<h2 style='text-align:center;'>Bar Chart</h2>", unsafe_allow_html=True)
            fig_bar_chart = plt.figure()
            plt.bar(bar_x, bar_x * 10)
            plt.xlabel('Categories')
            plt.ylabel('Values')
            st.pyplot(fig_bar_chart)

            # Add a download button for the bar chart
            buf_bar_chart = download_plot(fig_bar_chart)
            st.download_button("Download Bar Chart as PNG", buf_bar_chart, "bar_chart.png", "image/png")

        # Horizontal Bar Chart
        elif graph_options == "Horizontal Bar Chart":
            st.markdown("<h2 style='text-align:center;'>Horizontal Bar Chart</h2>", unsafe_allow_html=True)
            fig_horizontal_bar_chart = plt.figure()
            plt.barh(bar_x, bar_x * 10)
            plt.xlabel('Values')
            plt.ylabel('Categories')
            st.pyplot(fig_horizontal_bar_chart)

            # Add a download button for the horizontal bar chart
            buf_horizontal_bar_chart = download_plot(fig_horizontal_bar_chart)
            st.download_button("Download Horizontal Bar Chart as PNG", buf_horizontal_bar_chart, "horizontal_bar_chart.png", "image/png")

        # Scatter Plot
        elif graph_options == "Scatter Plot":
            st.markdown("<h2 style='text-align:center;'>Scatter Plot</h2>", unsafe_allow_html=True)
            fig_scatter_plot = plt.figure()
            plt.scatter(scatter_x, scatter_y, c='blue', alpha=0.5)
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            st.pyplot(fig_scatter_plot)

            # Add a download button for the scatter plot
            buf_scatter_plot = download_plot(fig_scatter_plot)
            st.download_button("Download Scatter Plot as PNG", buf_scatter_plot, "scatter_plot.png", "image/png")

            # Statistics
            st.write(f"Mean X: {np.mean(scatter_x):.2f}")
            st.write(f"Mean Y: {np.mean(scatter_y):.2f}")
            st.write(f"Standard Deviation X: {np.std(scatter_x):.2f}")
            st.write(f"Standard Deviation Y: {np.std(scatter_y):.2f}")
