import os
import glob
import json
import pandas as pd
import streamlit as st
from database import showDengueReports, remove_report, get_all_users, remove_user

def admin_panel():
    st.header("Admin Panel")
    
    # --- Reupload Dengue JSON Data ---
    st.subheader("Reupload Dengue JSON Data")
    uploaded_file = st.file_uploader("Upload new Dengue Clusters JSON file", type=["geojson"], key="admin_upload")
    if uploaded_file is not None:
        new_data = json.load(uploaded_file)
        with open("DengueClustersGEOJSON.geojson", "w") as f:
            json.dump(new_data, f, indent=4)
        st.success("Dengue clusters updated from uploaded JSON file.")
    
    # --- Load Reports ---
    reports = showDengueReports()  # Returns a list of report dicts
    if not reports:
        st.info("No reports available.")
    else:

        # Build a DataFrame from the reports
        df = pd.DataFrame(reports)
        
        # Add a column for interactive deletion
        df["Remove?"] = False

        def get_image_link(row):
            if row.get("report_type") == "Report Location":
                report_id = row.get("report_id")
                username = row.get("username")
                if not (report_id and username):
                    return "No Image1" #debug
                pattern = os.path.join("images", f"{username}_{report_id}.*")
                image_files = glob.glob(pattern)
                if image_files:
                    return f"<a href='?report_id={report_id}' target='_blank'>View Image</a>"
                else:
                    return "No Image" #debug
            return ""
        df["Image"] = df.apply(get_image_link, axis=1)
        
        # --- Display a combined view in two side-by-side columns ---
        if not df.empty and "username" in df.columns:
            max_username_len = df["username"].astype(str).map(len).max()
            # For instance, make col1 at least 1.5 and increase it based on the username length.
            col1_ratio = max(1.2, (max_username_len / 10))
        else:
            col1_ratio = 1.2
        
        # Create two columns with a dynamic ratio.
        col1, col2 = st.columns([col1_ratio, 1])
        
        with col1:
            st.subheader("Select Report(s) to Delete")
            columns_for_deletion = ["report_id", "username", "report_type", "date","latitude",'longitude', "Remove?"]
            df_deletion = df[columns_for_deletion]
            # Use st.data_editor for interactive deletion checkboxes.
            edited_df = st.data_editor(df_deletion, num_rows="dynamic", key="report_table")
            if st.button("Remove Selected Reports", key="remove_selected_btn"):
                rows_to_remove = edited_df[edited_df["Remove?"] == True]
                if not rows_to_remove.empty:
                    for _, row in rows_to_remove.iterrows():
                        remove_report(row["report_id"])
                        remove_report_images(row["report_id"], row["username"])
                    st.success("Selected report(s) removed.")
                    st.rerun()
                else:
                    st.warning("Please select at least one report to remove.")
        
        with col2:
            st.subheader("Image Viewer")
            # Render a read-only HTML table showing the Image column.
            # We show only a subset of columns for clarity.
            columns_to_show = ["report_id", "Image"]
            table_html = df[columns_to_show].to_html(escape=False, index=False)
            # Replace <th> with a centered version.
            table_html = table_html.replace("<th>", "<th style='text-align: center;'>")
            st.markdown(table_html, unsafe_allow_html=True)

    # --- New Feature: Delete User Accounts ---
    st.subheader("Delete User Accounts")
    users = get_all_users()
    if not users:
        st.info("No users available.")
    else:
        df_users = pd.DataFrame(users)
        df_users["Remove?"] = False
        # Display only user ID and username.
        df_users = df_users[['id', 'username', 'Remove?']]
        edited_users = st.data_editor(df_users, num_rows="dynamic", key="users_table")
        if st.button("Remove Selected Users", key="remove_users_btn"):
            rows_to_remove = edited_users[edited_users["Remove?"] == True]
            if not rows_to_remove.empty:
                for _, row in rows_to_remove.iterrows():
                    remove_user(row["id"])
                st.success("Selected user(s) removed.")
                st.rerun()
            else:
                st.warning("Please select at least one user to remove.")

def view_report_image():
    query_params = st.query_params  # st.query_params is used as a property.
    if "report_id" in query_params:
        report_id = query_params["report_id"][0]
        reports = showDengueReports()
        report = next((r for r in reports if str(r.get("report_id")) == report_id), None)
        if report and report.get("report_type") == "Report Location":
            image_filename = report.get("image_filename")
            if image_filename:
                img_path = os.path.join("images", image_filename)
                st.image(img_path, caption=f"Image for Report ID {report_id}")
            else:
                st.info("No image found for this report.")
        st.stop()

def remove_report_images(report_id, username):
    """
    Remove all image files that match the pattern for the given report.
    """
    pattern = os.path.join("images", f"{username}_{report_id}.*")
    image_files = glob.glob(pattern)
    for image_file in image_files:
        try:
            os.remove(image_file)
        except Exception as e:
            print(f"Error removing {image_file}: {e}")
