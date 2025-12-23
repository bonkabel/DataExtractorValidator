import streamlit as st
import pandas as pd
import os
import tempfile
import json
import plotly.express as px

from App import App
from app.Fields import Fields


def displayValidRecords(output):
    """Display the valid records content"""
    st.subheader("Valid Records")
    csvPath = os.path.join(output, "valid_records.csv")

    if os.path.exists(csvPath):
        df = pd.read_csv(csvPath)
        st.dataframe(df, use_container_width=True, hide_index=True)

        with open(csvPath, "rb") as f:
            st.download_button(
                label="Download Valid Records (CSV file)",
                data=f,
                file_name="valid_records.csv",
                mime="text/csv"
            )
    else:
        st.warning("No valid records found")

def displayReport(output):
    """Display the error report content"""
    st.subheader("Error Report")
    reportPath = os.path.join(output, "error_report.txt")

    if os.path.exists(reportPath):
        with open(reportPath, "r") as f:
            reportContent = f.read()

        st.code(reportContent, language=None)


        st.download_button(
            label="Download Error Report",
            data=reportContent,
            file_name="error_report.txt",
            mime="text/plain"
        )
    else:
        st.warning("No error report found")

def displayStatistics(output):
    """Display the statistics content"""
    st.subheader("Statistics")
    jsonPath = os.path.join(output, "statistics.json")

    if os.path.exists(jsonPath):
        with open(jsonPath, "r") as f:
            data = json.load(f)

        summary = data["summary"]

        # Row
        col1, col2, col3, col4, = st.columns(4)
        with col1:
            st.metric("Total Records", summary["totalRecordsProcessed"])
        with col2:
            st.metric("Valid Records", summary["validRecords"])
        with col3:
            st.metric("Invalid Records", summary["invalidRecords"])
        with col4:
            st.metric("Percent Valid", f"{summary['percentRecordsValid']:.1f}%")

        st.divider()

        # Row
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Validation Issues**")
            issuesdf = pd.DataFrame(
                list(data["validationIssues"].items()),
                columns=["Issue Type", "Count"]
            )

            fig1 = px.bar(issuesdf, x="Issue Type", y="Count")
            fig1.update_yaxes(tick0=0, dtick=1)

            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown("**Fields With Issues**")
            fieldsdf = pd.DataFrame(
                list(data["fieldsWithIssues"].items()),
                columns=["Field", "Count"]
            )
            fieldsdf["Field"] = fieldsdf["Field"].apply(Fields.getDisplayName)
            fig2 = px.bar(fieldsdf, x="Field", y="Count")
            fig2.update_yaxes(tick0=0, dtick=1)
            st.plotly_chart(fig2, use_container_width=True)

        with col3:
            # Pie chart
            st.markdown("**Record Distribution**")
            pieData = pd.DataFrame({
                "Status": ["Valid", "Invalid"],
                "Count": [summary["validRecords"], summary["invalidRecords"]]
            })
            fig3 = px.pie(pieData, values="Count", names="Status",
                          color="Status",
                          color_discrete_map={"Valid": "#10b981", "Invalid": "#ef4444"},
                          hole=0.3)
            fig3.update_traces(
                textposition="inside",
                texttemplate="%{percent}",
                textfont_size=18,
                textfont_color="black",
                hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
            )
            fig3.update_layout(showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

        # Timestamp
        st.caption(f"Generated: {summary["timestamp"]}")

    else:
        st.warning("No statistics found")

def run(inputPDF, outputDirectory):
    """Run the app"""
    try:
        with st.spinner("Processing PDF..."):
            app = App(inputPDF, outputDirectory)
            app.run()
    except Exception as e:
        st.exception(e)

st.set_page_config(
    page_title="Patient Data Extractor",
    layout="wide"
)

st.title("Patient Data Extractor")
st.markdown("Upload a PDF to extract and validate patient records")


uploadedFile = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploadedFile is not None:
    with tempfile.TemporaryDirectory() as tmpDir:
        # Save the file
        inputPDF = os.path.join(tmpDir, uploadedFile.name)
        with open(inputPDF, "wb") as f:
            f.write(uploadedFile.getbuffer())

        # Create output directory
        outputDirectory = os.path.join(tmpDir, "output")
        os.makedirs(outputDirectory, exist_ok=True)

        # Run the app
        run(inputPDF, outputDirectory)

        tab1, tab2, tab3 = st.tabs(["Valid Records", "Statistics", "Error Report"])

        with tab1:
            displayValidRecords(outputDirectory)

        with tab2:
            displayStatistics(outputDirectory)

        with tab3:
            displayReport(outputDirectory)