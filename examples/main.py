from linkedin_api import Linkedin
import pandas as pd
from fastapi import FastAPI , File, UploadFile, BackgroundTasks

import re

app = FastAPI()
# Authenticate using any Linkedin account credentials
api = Linkedin('disamex883@vasteron.com', 'Testing@123')

def extract_linkedin_name(linkedin_url):
    # Define a regular expression pattern to match the name part of the URL
    pattern = r'/in/([^/]+)/?'

    # Search for the pattern in the LinkedIn URL
    match = re.search(pattern, linkedin_url)

    # If a match is found, return the name; otherwise, return None
    return match.group(1) if match else None

def add_data_to_excel(file_path, new_data):
    # Check if the Excel file already exists
    file_exists = False
    try:
        df_existing = pd.read(file_path)
        file_exists = True
    except FileNotFoundError:
        pass

    # Create a DataFrame from the new data
    df_new = pd.DataFrame([new_data])

    # Concatenate the existing DataFrame and the new DataFrame
    df_combined = pd.concat([df_existing, df_new], ignore_index=True) if file_exists else df_new

    # Write the combined DataFrame to the Excel file
    # df_combined.to_excel(file_path, index=False)
    df_combined.to_csv(file_path, index=False)


def dataAdd():
    df= pd.read_excel('linkedindata.xlsx')
    data = df.to_dict(orient='records')

    for i in data:
        name = i['Name']
        profile = api.get_profile(name)
        new_data = {"LinkedInData": profile, "Name": name}
        add_data_to_excel('linkedinextract.csv', new_data)

@app.get("/")
async def read_root(background_tasks: BackgroundTasks):
    background_tasks.add_task(dataAdd)
    return {"Hello": "World"}
    
@app.post("/")
async def upload_csv(file: UploadFile ):
     # Check if the uploaded file is a CSV file
        
    if file.filename.endswith('.xlsx'):
        # Read the content of the Excel file
        # print(file.file)
        contents = file.file.read()
        df = pd.read_excel(contents)


        # # Process the dataframe as needed

        data = df.to_dict(orient='records')

        # store all linkedin url in a file 
        for i in data:
            linkedin_url = i['Linkedin']
            name = extract_linkedin_name(linkedin_url)
            if name:
                print(f"LinkedIn Name: {name}")
        
                # Assuming you want to add the LinkedIn URL and Name to the Excel file
                excel_file_path = 'linkedindata.xlsx'
                new_data = {"LinkedIn": linkedin_url, "Name": name}
                add_data_to_excel(excel_file_path, new_data)
            else:
                print("Invalid LinkedIn URL or Name not found.")

        return {"filename": file.filename, "data": data}
    else:
        return {"error": "Uploaded file must be an xlsx file"}
    
@app.get("/data/{user_id}")
async def read_data(user_id: str):
    # get from req params 
    print(user_id)
    data = api.get_profile(user_id)
    print(data)
    return data