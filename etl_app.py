import streamlit as st
#File processing
from PIL import Image
import pandas as pd
import docx2txt
from PyPDF2 import PdfReader as PdfFileReader
import pdfplumber
import os

Page_config = {"page_title": " THE ANH VU", "layout": "wide", "initial_sidebar_state": "auto"}
def text_to_csv():

	col1, col2, col3, col4, col5 = st.columns(5)
	with col1:
		myrows = int(st.number_input("Skip Row"))
	with col2:
		myINT_NaN = st.number_input("Replace INT/Float to -999.255")
	with col3:
		myString_NaN= st.text_input('Replace String to NULL')

	with col4:
		myFK1 = st.number_input("Add FK1 INT")

	with col5:
		myFK2 = st.number_input("Add FK2 INT")

	data_file = st.file_uploader("Upload text", type =["txt"])
	
	
	if data_file is not None:
		file_details ={"filename": data_file.name, "filetype": data_file.type, "filesize": data_file.size}
		st.write(file_details)
		if data_file.type =="text/plain":
			dataframe = pd.read_csv(data_file, skiprows=myrows, sep='\s+', header=None)
			dataframe = dataframe.replace(myINT_NaN, -999.255)
			dataframe = dataframe.replace(myString_NaN, "NULL")
			dataframe['FK1'] = int(myFK1)
			dataframe['FK2'] = int(myFK1)

		else:
			dataframe=pd.DataFrame()
			st.write('File Type is not readable')

	else:
		dataframe=pd.DataFrame()


	
	st.dataframe(dataframe, use_container_width=True)
	csv = dataframe.to_csv().encode('utf-8')
	col1, col2= st.columns(2)
	with col1:
		st.download_button(
	    label="Download data as .CSV",
	    data=csv,
	    file_name='Theanh.csv',
	    mime='text/csv',)

	with col2:
		st.download_button(
	    label="Download data as .TXT",
	    data=csv,
	    file_name='Theanh.txt',
	    mime='text/csv',)

def main():
	st.title("ICG Well data ELT")
	st.subheader("Copy right @ The Anh Vu")
	submenu = ["ELT", "About Me"]
	choice = st.sidebar.selectbox("Sub Menu",submenu )
	text_to_csv()

if __name__ == '__main__':
	main()

