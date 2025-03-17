from genericpath import exists
import pandas
import asyncio
import aiohttp
import os
from tqdm import tqdm

excel_file = "./data/GRI_2017_2020 (1).xlsx"
output_folder = "./download/"


# Extract the report names from the excel file
def extract_report_names(excel_file: str):
    excel = pandas.read_excel(excel_file, sheet_name=0)
    num_cells = len(excel["BRnum"].values)

    rapport_names = zip(
        excel["BRnum"].values,
        excel["Pdf_URL"].values,
        excel["Report Html Address"].values,
    )
    return rapport_names, num_cells


async def download_file(session: aiohttp.ClientSession, tuple_data) -> str:
    filename, link1, link2 = tuple_data
    outname = output_folder + filename + ".pdf"

    # Don't download existing reports
    if exists(outname):
        return f"1\t{filename}\n"

    # Empty cells become 'float', for some reason
    link1 = None if type(link1) is float else link1
    link2 = None if type(link2) is float else link2

    # Try links
    for link in [link1, link2]:
        if not link:
            continue

        try:
            async with session.get(link, chunked=True, raise_for_status=True) as response:
                try:
                    with open(outname, "wb") as file:
                        file.write("abc".encode())  # don't bother downloading the file
                        #file.write(response.content)
                    return f"1\t{filename}\n"
                except Exception as e:
                    os.remove(outname)
                    return f"3\t{filename}\tfile exception {e}\n"
        except aiohttp.ClientResponseError as e:
            return f"2\t{filename}\thttp exception {e.status} - {e.message}\n"
        except Exception as e:
            return f"2\t{filename}\t{e}\n"

    return ""#f"0\t{filename}"


async def download_all_files():
    if not exists(excel_file):
        print(f'"{excel_file}" was not found!')
        exit(1)

    if not exists(output_folder):
        os.mkdir(output_folder)

    report_data, count = extract_report_names(excel_file)

    connector=aiohttp.TCPConnector(limit=25)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [download_file(session, tuple_data) for tuple_data in report_data]

        with open("report.csv", "wt") as report:
            for f in tqdm(asyncio.as_completed(tasks), desc="Henter pdf filer", unit=" pdf", total=count):
                report.write(await f)


if __name__ == "__main__":
    asyncio.run(download_all_files())
