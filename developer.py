import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Function to convert graphs to PNG and download
def download_plot(fig, filename="plot.png"):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Developer dashboard function with graphs
def show_developer_dashboard():
    st.markdown("<h1 style='text-align:center;'>Developer Dashboard</h1>", unsafe_allow_html=True)

    # Data for the graphs
    x = np.linspace(0, 10, 100)
    bar_x = np.array([1, 2, 3, 4, 5])
    scatter_x = np.random.rand(100)
    scatter_y = np.random.rand(100)

    # Sidebar graph options
    if 'dev_graph_option' not in st.session_state:
        st.session_state.dev_graph_option = "Line Chart"

    st.sidebar.markdown("## Choose a graph")
    graph_options = st.sidebar.radio(
        "Select a graph:",
        options=("Line Chart", "Bar Chart", "Horizontal Bar Chart", "Scatter Plot"),
        index=["Line Chart", "Bar Chart", "Horizontal Bar Chart", "Scatter Plot"].index(st.session_state.dev_graph_option)
    )
    st.session_state.dev_graph_option = graph_options  # Update session state

    # Use a container
    with st.container():
        # Line Chart
        if graph_options == "Line Chart":
            st.markdown("<h2 style='text-align:center;'>Line Chart</h2>", unsafe_allow_html=True)
            fig_line_chart = plt.figure()
            plt.plot(x, np.sin(x), color='blue', label='sin(x)')
            plt.plot(x, np.cos(x), color='green', label='cos(x)')
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

    # Navigation to Analyst Dashboard - Sidebar Bottom Section
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("<h3 style='text-align:center;'>Want to switch to the Analyst Dashboard?</h3>", unsafe_allow_html=True)
    if st.sidebar.button("Go to Analyst Dashboard"):
        st.session_state.page = 'analyst'
