import requests
import json
import pandas as pd
import plotly.express as px

class VacancyData:
    def __init__(self, url):
        self.url = url
        self.df = None

    def fetch_data(self):
        try:
            response = requests.get(self.url, verify=False)
            response.raise_for_status()
            data = response.text.split('"result":')[1].split('"}]')[0] + '"}]'
            results = json.loads(data)
            self.df = pd.DataFrame({
                "Vacancy Name": [result.get("vacancy_name") for result in results],
                "Tenant Name": [result.get("tenant_name") for result in results],
                "Jenjang": [result.get("jenjang") for result in results],
                "Stream Name": [result.get("stream_name") for result in results],
                "Jurusan Name": [result.get("jurusan_name") for result in results],
                "jurusan_filter_type": [result.get("jurusan_filter_type") for result in results],
                "total_job_availables": [result.get("total_job_available") for result in results],
                "check_certificates": [result.get("check_certificate") for result in results],
                "major_group_non_sma": [result.get("major_group_non_sma") for result in results],
                "major_group_sma": [result.get("major_group_sma") for result in results],
                "allow_sma": [result.get("allow_sma") for result in results],
                "highest_age_sma": [result.get("highest_age_sma") for result in results],
                "lowest_ipk_sma": [result.get("lowest_ipk_sma") for result in results],
                "allow_d3": [result.get("allow_d3") for result in results],
                "highest_age_d3": [result.get("highest_age_d3") for result in results],
                "lowest_ipk_d3": [result.get("lowest_ipk_d3") for result in results],
                "allow_s1": [result.get("allow_s1") for result in results],
                "highest_age_s1": [result.get("highest_age_s1") for result in results],
                "lowest_ipk_s1": [result.get("lowest_ipk_s1") for result in results],
                "allow_s2": [result.get("allow_s2") for result in results],
                "highest_age_s2": [result.get("highest_age_s2") for result in results],
                "lowest_ipk_s2": [result.get("lowest_ipk_s2") for result in results],
                "vacancy_types": [result.get("vacancy_type") for result in results],
                "major_sma_customs": [result.get("major_sma_custom") for result in results],
                "major_non_sma_customs": [result.get("major_non_sma_custom") for result in results]
            })
            self.df['highest_age_s1'].fillna(0, inplace=True)
            self.df['highest_age_s1'] = self.df['highest_age_s1'].astype(int)
            return True
        except requests.exceptions.RequestException as e:
            print("Error fetching data:", e)
            return False

    def plot_avg_highest_age_s1(self):
        if self.df is None:
            print("Data not fetched yet. Fetch data first.")
            return
        avg_highest_age_s1 = self.df.groupby("Stream Name")["highest_age_s1"].mean().reset_index()
        fig = px.bar(avg_highest_age_s1, x='Stream Name', y='highest_age_s1', title='Average Highest Age S1 for Each Stream Name')
        fig.show()

    def save_data_as_excel(self, file_path):
        if self.df is None:
            print("Data not fetched yet. Fetch data first.")
            return
        try:
            self.df.to_excel(file_path, index=False)
            print("DataFrame saved as Excel file:", file_path)
        except Exception as e:
            print("Error saving data:", e)

if __name__ == "__main__":
    url = "https://rekrutmenbersama2024.fhcibumn.id/job/loadRecord/"
    vacancy_data = VacancyData(url)
    if vacancy_data.fetch_data():
        print(vacancy_data.df)
        vacancy_data.plot_avg_highest_age_s1()
        file_path = r"D:\vacancy_data.xlsx"
        vacancy_data.save_data_as_excel(file_path)
