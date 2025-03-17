
excel_file = "../data/GRI_2017_2020 (1).xlsx"
output_folder = "./download/"

from genericpath import exists
import requests
import pandas
import certifi
import ssl


# Extract the report names from the excel file
def extract_report_names(excel_file: str):
    df = pandas.read_excel(excel_file, sheet_name=0)
    rapport_names = zip(
       df["BRnum"].values,
       df["Pdf_URL"].values,
       df["Report Html Address"].values
    )
    return rapport_names


def download_file(session: requests.Session, filename: str, link1: str, link2: str) -> bool:
    outname = output_folder + filename + ".pfd"

    # Don't download existing reports
    if exists(outname):
        return

    # Empty cells become 'float', for some reason
    link1 = None if type(link1) is float else link1
    link2 = None if type(link2) is float else link2

    # Try links
    for link in [link1, link2]:
        if not link:
            continue

        try:
            with session.get(link, cert=certifi.where()) as response:
                response.raise_for_status()
                with open(outname, "wb") as file:
                    file.write(response.content)
                print(f'{filename} 1')
                return True
        except Exception as e:
            #print(f"Error downloading {link}: {e}")
            pass

    print(f'{filename} 0')
    return False


if __name__ == "__main__":
    if not exists(excel_file):
        print(f'"{excel_file}" was not found!')
        exit(1)

    if not exists(output_folder):
        os.mkdir(output_folder)

    report_data = extract_report_names(excel_file)
    count = 4
    index = 0

    with requests.Session() as session:
        for filename, l1, l2 in report_data:
            if index >= count:
                break

            success = download_file(session, filename, l1, l2)
            index += 1
