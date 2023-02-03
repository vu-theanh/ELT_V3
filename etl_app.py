import streamlit as st
#File processing
from PIL import Image
import pandas as pd
import docx2txt
from PyPDF2 import PdfReader as PdfFileReader
import pdfplumber
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

Page_config = {"page_title": " THE ANH VU", "layout": "wide", "initial_sidebar_state": "auto"}
st.set_page_config(**Page_config)
def text_to_csv():

	col1, col2, col3, col4 = st.columns(4)
	with col1:
		myrows = int(st.number_input("Skip Row", value = 0))

	with col2:
		myFK1 = st.number_input("RUN", value = 1)

	with col3:
		myFK2 = st.number_input("SET", value = 1)

	with col4:
		myFK3 = st.text_input("WELL_NAME", value = "WELL_NAME")

	data_file = st.file_uploader("Upload Your File", type =["txt"])

	
	
	if data_file is not None:
		file_details ={"filename": data_file.name, "filetype": data_file.type, "filesize": data_file.size}
		if st.checkbox("Header: "):
			header_line = 0
		else:
			header_line = None

		if data_file.type =="text/plain":
			try:
				dataframe = pd.read_csv(data_file, skiprows=myrows, sep = "\s+", skipinitialspace=True, header=header_line)
				# dataframe = dataframe.replace(myINT_NaN, -999.255)
				# dataframe = dataframe.replace(myString_NaN, "NULL")
				dataframe['RUN'] = int(myFK1)
				dataframe['SET'] = int(myFK2)
				dataframe['WELL_NAME'] = myFK3
			except:
				dataframe=pd.DataFrame()
				st.warning("Your Text File contain special characters, please remove it Or select greater skip Row")
		else:
			dataframe=pd.DataFrame()
			st.write('File Type is not readable')

	else:
		dataframe=pd.DataFrame()

	st.dataframe(dataframe.head(100), use_container_width=True)



	#Attach header

	header_input = st.text_area("Your Header Here optional, separator = Comma and Space", value = "header")
	header_list = '{}'.format(header_input) + ", RUN, SET, WELL_NAME"
	header = header_list.split(", ")
	st.write(len(header), len(list(dataframe)))
	# test header read:
	

	if len(header) == len(list(dataframe)) and len(header) >0:
		dataframe_rename = dataframe.set_axis(header,axis=1)
	else:
		st.warning("Checking you header")
		dataframe_rename =dataframe

	st.dataframe(dataframe_rename.head(5), use_container_width=True)

	csv = dataframe.to_csv(header=True, index=False).encode('utf-8')
	col1, col2= st.columns(2)


	myname = st.text_input("File_Name", value = "File Name", label_visibility="hidden")
	with col1:
		st.download_button(
	    label="Download data as .CSV",
	    data=csv,
	    file_name='Welllog_{}.csv'.format(myname),
	    mime='text/csv',)

	with col2:
		st.download_button(
	    label="Download data as .TXT",
	    data=csv,
	    file_name='Welllog_{}.txt'.format(myname),
	    mime='text/csv',)

def header_process():
	header_input = st.text_area("Your Header Section Here", value = "header")
	header_list = '{}'.format(header_input)
	header = header_list.split(", ")
	
	# test header read:

	data = header_input
	#df = pd.DataFrame(data.split(":"))
	try:
		df = pd.DataFrame([x.split(' .') for x in data.split('\n')])
		df2 = df[1].str.split(':', expand=True)
		df[1] = df2[0]
		df[2]=df2[1]
	except:
		st.write(" Separator should be LAS 2.0 format: 'Space Comma' then ':' ")
		df = pd.DataFrame()
		
	st.dataframe(df, use_container_width=True)

	csv = df.to_csv(header=True, index=False).encode('utf-8')

	checkbox = st.checkbox("Log Header/Well Header")
	myname = st.text_input("Well Name", value = "well name", label_visibility="hidden")

	if checkbox:
		my_file_name = "Log_header_{}".format(myname)
	else:
		my_file_name = "Well_header_{}".format(myname)

	st.download_button(
	label="Download file as .csv",
	data=csv,
	file_name=my_file_name,
	mime='text/csv',)

def box_plot(df, selection):

	vars = selection
	if len(vars)>0:
		fig =make_subplots(rows =1, cols = len(vars))
		for i, var in enumerate(vars):
			fig.add_trace(
				go.Box(y = df[var],
					name = var),
				row =1, col = i+1)
		st.plotly_chart(fig, use_container_width=True)

def Chart():

	data_file = st.file_uploader("Upload Your download CSV to QC", type =["csv"])

	if data_file is not None:
		file_details ={"filename": data_file.name, "filetype": data_file.type, "filesize": data_file.size}
		st.write(type(data_file))
		df = pd.read_csv(data_file)
		st.dataframe(df)
	else:
		df = pd.DataFrame()

	st.info("This show chart of selected data. Just select as using to saving the memory")
	
	axis_list = list(df)
	vars = st.multiselect("Select multiple data to plot",axis_list, key = 23)
	box_plot(df, vars)

def main():
	st.title("ICG Well data ELT")
	st.subheader("@ The Anh Vu")
	submenu = ["LAS FILE FORMATER", "Header Process", "Box Plot"]
	choice = st.sidebar.selectbox("Sub Menu",submenu )
	if choice == "LAS FILE FORMATER":
		st.info("Save your LAS file as .TXT type co clean convert it to SQL, PtSQL, Petrel, Techlog.. loadable format ")
		text_to_csv()
	elif choice == "Header Process":
		st.info("Past your header section here to convert to column CSV format ")
		header_process()
	else:
		Chart()

if __name__ == '__main__':
	main()

