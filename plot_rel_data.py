import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from io import StringIO


def plot_file(fname):
    df = pd.read_csv(fname)

    # If there's no data, return
    if df.empty:
        st.error("File empty, no data to plot.")
        return

    plt_title = fname.name

    df["Datetime"] = df["Date/Time"].str.split(" \\(").str.get(0)  # type: ignore
    df.index = pd.to_datetime(df["Datetime"])  # type: ignore
    df = df.drop(columns=["Date/Time", "Datetime"])  # type: ignore
    fig = px.line(df, x=df.index, y=df.columns)
    # Set the title of the graph
    fig.update_layout(title_text=plt_title)
    # Set axis labels
    fig.update_xaxes(title_text="Datetime")
    fig.update_yaxes(title_text="Temperature (degC)")
    # Set legend title
    fig.update_layout(legend_title="Temperature Sensor")
    # set comparison mode
    fig.update_layout(hovermode="x")
    st.plotly_chart(fig, theme=None, use_container_width=True, height=800)

    if st.button("Open graph in new tab"):
        fig.show()

    html_fname = f"{plt_title[:-4]}.html"
    html_buffer = StringIO()
    fig.write_html(html_buffer)

    st.download_button(
        label="Download interactive graph",
        data=html_buffer.getvalue(),
        file_name=html_fname,
        mime="text/html",
    )


def main():
    pio.templates.default = "plotly"  # important - fixes streamlit bug with plotly

    st.title("Rel Testing Data Plotter")

    uploaded_files = st.file_uploader(
        "Upload files", accept_multiple_files=True, type=([".csv"])
    )
    if uploaded_files is not None:
        # fnames = [f.name for f in uploaded_files]
        selected_file = st.selectbox(
            "Select a data file to plot",
            uploaded_files,
            index=0,
            format_func=lambda x: x.name if x is not None else "Upload files first",
            key="file_select",
            placeholder="Upload files first",
        )
        if selected_file is not None:
            plot_file(selected_file)


if __name__ == "__main__":
    main()
