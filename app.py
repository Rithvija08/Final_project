import streamlit as st
import os
from datetime import datetime

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Document Management System",
    page_icon="📄",
    layout="wide"
)

# ---------------- FOLDER ----------------

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------- SIDEBAR ----------------

st.sidebar.title("📋 Document Management")

menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Home",
        "📤 Upload Document",
        "📁 My Documents"
    ]
)


# =========================================================
# HOME
# =========================================================

if menu == "🏠 Home":

    st.title("📄 Document Management System")

    st.write(
        "Manage your documents easily."
    )

    files = os.listdir(UPLOAD_FOLDER)

    st.metric(
        "Total Documents",
        len(files)
    )


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

elif menu == "📤 Upload Document":

    st.title("📤 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF document",
        type=["pdf"]
    )

    if uploaded_file is not None:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(
            f"✅ {uploaded_file.name} uploaded successfully!"
        )
# =========================================================
# MY DOCUMENTS
# =========================================================

elif menu == "📁 My Documents":

    st.title("📁 My Documents")

    files = os.listdir(UPLOAD_FOLDER)

    # Get only PDF files
    pdf_files = [
        file for file in files
        if file.lower().endswith(".pdf")
    ]

    # No documents
    if not pdf_files:

        st.info("📂 No PDF documents uploaded yet.")

    else:

        # =================================================
        # CREATE TABS
        # =================================================

        tab1, tab2, tab3 = st.tabs(
            [
                "🔍 Search",
                "👀 Preview",
                "🗑️ Delete"
            ]
        )

        # =================================================
        # SEARCH TAB
        # =================================================

        with tab1:

            # Check whether a PDF is selected
            if "selected_pdf" not in st.session_state:

                st.subheader("🔍 Search Documents")

                search = st.text_input(
                    "Search PDF",
                    placeholder="Enter document name..."
                )

                if search:

                    results = [
                        file
                        for file in pdf_files
                        if search.lower() in file.lower()
                    ]

                    if results:

                        st.success(
                            f"Found {len(results)} document(s)"
                        )

                        for file in results:

                            if st.button(
                                f"📄 {file}",
                                key=f"open_{file}"
                            ):

                                st.session_state.selected_pdf = file
                                st.rerun()

                    else:

                        st.warning(
                            "❌ No matching documents found."
                        )

                else:

                    st.write(
                        "Enter a document name to search."
                    )

            # =================================================
            # PDF VIEWER
            # =================================================

            else:

                selected_file = (
                    st.session_state.selected_pdf
                )

                file_path = os.path.join(
                    UPLOAD_FOLDER,
                    selected_file
                )

                st.title(f"📄 {selected_file}")

                # Back button
                if st.button("⬅️ Back to Search"):

                    del st.session_state.selected_pdf

                    st.rerun()

                st.divider()

                # Open PDF
                with open(
                    file_path,
                    "rb"
                ) as pdf_file:

                    pdf_data = pdf_file.read()

                st.pdf(
                    pdf_data,
                    height=900
                )

        # =================================================
        # PREVIEW TAB
        # =================================================

        with tab2:

            st.subheader("👀 Preview Document")

            selected_file = st.selectbox(
                "Select a PDF",
                pdf_files
            )

            if selected_file:

                file_path = os.path.join(
                    UPLOAD_FOLDER,
                    selected_file
                )

                st.write("### 📋 Document Information")

                file_size = os.path.getsize(
                    file_path
                )

                from datetime import datetime

                modified_time = os.path.getmtime(
                    file_path
                )

                modified_date = datetime.fromtimestamp(
                    modified_time
                ).strftime("%d-%m-%Y %H:%M:%S")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write("**File Name**")
                    st.write(selected_file)

                with col2:
                    st.write("**File Size**")
                    st.write(
                        f"{file_size / 1024:.2f} KB"
                    )

                with col3:
                    st.write("**Last Modified**")
                    st.write(modified_date)

                st.divider()

                with open(
                    file_path,
                    "rb"
                ) as pdf_file:

                    pdf_data = pdf_file.read()

                st.pdf(
                    pdf_data,
                    height=700
                )

        # =================================================
        # DELETE TAB
        # =================================================

        with tab3:

            st.subheader("🗑️ Delete Document")

            delete_file = st.selectbox(
                "Select PDF to delete",
                pdf_files
            )

            st.warning(
                f"⚠️ Selected document: **{delete_file}**"
            )

            confirm = st.checkbox(
                "I confirm that I want to delete this document."
            )

            if confirm:

                if st.button(
                    "🗑️ Delete Document",
                    type="primary"
                ):

                    file_path = os.path.join(
                        UPLOAD_FOLDER,
                        delete_file
                    )

                    os.remove(file_path)

                    st.success(
                        f"✅ {delete_file} "
                        "was deleted successfully!"
                    )

                    st.rerun()