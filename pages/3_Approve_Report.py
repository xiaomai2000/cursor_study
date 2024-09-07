import streamlit as st
from batch_processor import approve_report

def main():
    st.title("Approve Report")
    if st.button("Approve Report"):
        if approve_report():
            st.success("Report approved successfully.")
            st.progress(100)
        else:
            st.error("Failed to approve report.")

if __name__ == "__main__":
    main()