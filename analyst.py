import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from layout import add_navbar

# Function to convert graphs to PNG and download
def download_plot(fig, filename="plot.png"):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Cached function for generating static data
@st.cache_data
def get_data():
    x = np.linspace(0, 10, 100)
    bar_x = np.array([1, 2, 3, 4, 5])
    scatter_x = np.random.rand(100)
    scatter_y = np.random.rand(100)
    return x, bar_x, scatter_x, scatter_y

# Function to handle page state changes and reruns
def handle_page_state(new_option):
    if st.session_state.graph_option != new_option:
        st.session_state.graph_option = new_option
        st.rerun()

# Analyst dashboard function with graphs
def show_analyst_dashboard():
    # Add the navigation bar
    add_navbar()

    # Page title
    st.markdown("<h1>Analyst Dashboard</h1>", unsafe_allow_html=True)

    # Get the cached data
    x, bar_x, scatter_x, scatter_y = get_data()

    # Sidebar graph options
    if 'graph_option' not in st.session_state:
        st.session_state.graph_option = "Line Chart"

    st.sidebar.markdown("## Choose a graph")
    graph_options = st.sidebar.selectbox(
        "Select a graph:",
        options=("Line Chart", "Bar Chart", "Horizontal Bar Chart", "Scatter Plot"),
        index=["Line Chart", "Bar Chart", "Horizontal Bar Chart", "Scatter Plot"].index(st.session_state.graph_option),
        key='graph_dropdown'
    )
    
    # Handle graph option change with state management
    handle_page_state(graph_options)

    # Use a container
    with st.container():
        # Split the page into three columns
        col1, col2, col3 = st.columns([1, 2, 1])  # Middle column is twice as wide

        with col2:  # Place the graphs in the middle column
            # Line Chart
            if graph_options == "Line Chart":
                st.markdown("<h2 >Line Chart</h2>", unsafe_allow_html=True)
                fig_line_chart = plt.figure(figsize=(5, 3))
                plt.plot(x, np.sin(x), color='blue', label='sin(x)')
                plt.plot(x, np.cos(x), color='green', label='cos(x)')
                plt.legend()
                st.pyplot(fig_line_chart)

                # Add a download button for the line chart
                buf_line_chart = download_plot(fig_line_chart)
                st.write("##")
                st.download_button("Download Line Chart", buf_line_chart, "line_chart.png", "image/png")

            # Bar Chart
            elif graph_options == "Bar Chart":
                st.markdown("<h2 >Bar Chart</h2>", unsafe_allow_html=True)
                fig_bar_chart = plt.figure(figsize=(5, 3))
                plt.bar(bar_x, bar_x * 10)
                plt.xlabel('Categories')
                plt.ylabel('Values')
                st.pyplot(fig_bar_chart)

                # Add a download button for the bar chart
                buf_bar_chart = download_plot(fig_bar_chart)
                st.write("##")
                st.download_button("Download Bar Chart", buf_bar_chart, "bar_chart.png", "image/png")

            # Horizontal Bar Chart
            elif graph_options == "Horizontal Bar Chart":
                st.markdown("<h2 >Horizontal Bar Chart</h2>", unsafe_allow_html=True)
                fig_horizontal_bar_chart = plt.figure(figsize=(5, 3))
                plt.barh(bar_x, bar_x * 10)
                plt.xlabel('Values')
                plt.ylabel('Categories')
                st.pyplot(fig_horizontal_bar_chart)

                # Add a download button for the horizontal bar chart
                buf_horizontal_bar_chart = download_plot(fig_horizontal_bar_chart)
                st.write("##")
                st.download_button("Download Horizontal Bar Chart", buf_horizontal_bar_chart, "horizontal_bar_chart.png", "image/png")

            # Scatter Plot
            elif graph_options == "Scatter Plot":
                st.markdown("<h2>Scatter Plot</h2>", unsafe_allow_html=True)
                fig_scatter_plot = plt.figure(figsize=(5, 3))
                plt.scatter(scatter_x, scatter_y, c='blue', alpha=0.5)
                plt.xlabel('X-axis')
                plt.ylabel('Y-axis')
                st.pyplot(fig_scatter_plot)

                # Add a download button for the scatter plot
                buf_scatter_plot = download_plot(fig_scatter_plot)
                st.write("##")
                st.download_button("Download Scatter Plot", buf_scatter_plot, "scatter_plot.png", "image/png")

                # Statistics in the right column
                with col3:
                    st.write("##")
                    st.write("##")
                    st.write("##")
                    st.write("Statistics")
                    st.write(f"**Mean**:     | X: {np.mean(scatter_x):.2f} | Y: {np.mean(scatter_y):.2f}")
                    st.write(f"**Median**:   | X: {np.median(scatter_x):.2f} | Y: {np.median(scatter_y):.2f}")
                    st.write(f"**Std Dev**:  | X: {np.std(scatter_x):.2f} | Y: {np.std(scatter_y):.2f}")
                    st.write(f"**Minimum**:  | X: {np.min(scatter_x):.2f} | Y: {np.min(scatter_y):.2f}")
                    st.write("**Maximum**:  | X: 5.00 | Y: 5.00")
                    st.write(f"**Variance**:  | X: {np.var(scatter_x):.2f} | Y: {np.var(scatter_y):.2f}")
                    
                    # Calculate IQR
                    q1_x, q3_x = np.percentile(scatter_x, [25, 75])
                    iqr_x = q3_x - q1_x
                    q1_y, q3_y = np.percentile(scatter_y, [25, 75])
                    iqr_y = q3_y - q1_y

                    st.write(f"**IQR**:      | X: {iqr_x:.2f} | Y: {iqr_y:.2f}")

if __name__ == "__main__":
    show_analyst_dashboard()
