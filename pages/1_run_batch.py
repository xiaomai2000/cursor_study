import streamlit as st
from batch_processor import run_batch

def main():
    st.title("Run Batch")
    folder_path = st.text_input("Select a folder:")
    if st.button("Run Batch"):
        if run_batch(folder_path):
            st.success("Batch processed successfully.")
        else:
            st.error("Batch processing failed.")

if __name__ == "__main__":
    main()