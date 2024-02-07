import streamlit as st
# import module
import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
# def add_numbers(num1, num2):
#     return num1 + num2
def scrapper( tag, Page):
    def getdata(url):
        r = requests.get(url)
        return r.text
    
    
    
    Title = []
    view = []
   
    
    for i in range(Page):
        st.success(f"Processing page : {i}", icon="✅")
        # url
        # url = "https://stackoverflow.com/questions/tagged/"+tag+"/?tab=votes&page="+str(page)
        url= "https://stackoverflow.com/questions/tagged/"+tag+"?tab=votes&page="+str(i)
        print(url)

        # pass the url
        # into getdata function
        htmldata = getdata(url)
        soup = BeautifulSoup(htmldata, 'html.parser')
        All = []
        # traverse author name
        for i in soup.find_all("h3", "s-post-summary--content-title"):
            All.append(i.get_text().split("\n"))
        View = []
        for i in soup.find_all("div", "s-post-summary--stats-item is-supernova"):
            View.append(i.get_text().split("\n"))
        for i in All:
            Title.append(i[-2])
        for i in View:
            view.append(i[1])
    if view!=Title:
        temp = len(view)-len(Title)
        for i in range(abs(temp)):
            view.append("NA")
    dic = {"Title": Title, "View":view}
    df = pd.DataFrame(dic) 
    
    
    @st.cache
    def convert_df_to_csv(df):
      # IMPORTANT: Cache the conversion to prevent computation on every rerun
      return df.to_csv().encode('utf-8')
    st.download_button(
      label="Download data as CSV",
      data=convert_df_to_csv(df),
      file_name='large_df.csv',
      mime='text/csv',
    )
    
    return("Hurrah!!!!!!! Completed")
def main():
    st.title("Scrapper App[Stackoverflow]")
    st.write("Enter Tag and  of pages to get the Result.")
    tag = st.text_input("Category: ")
    Page = st.number_input("Number of Pages :", step=1)
    
    val = st.text_input("User: ")
    users = ["user404", "Satyam_"]
    if st.button("Export to CSV"):
        if val in users:
            result = scrapper( tag, Page)
            st.success(result)
        else:
            st.success(f"Invalid Users : {val}", icon="🔴")
if __name__ == "__main__":
    main()
    
