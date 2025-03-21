from genericpath import exists
from tqdm import tqdm
from urllib.parse import urlparse
import asyncio
import aiohttp
import ssl
import urllib.parse
import pandas
import os

excel_file = "./data/GRI_2017_2020 (1).xlsx"
output_folder = "./download/"
max_retries = 3
url_timeout = 45.0
developer_mode = False

# Headers used to pretend we are a browser.
# Some sites reject requests if they do not look like
# they originate from a browser.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    # "Upgrade-Insecure-Requests": "1",
    "Accept-encoding": "gzip, deflate, zstd",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
}


def extract_report_names():
    """
    Extract the report names from the excel file.
    Returns a zip object and the total count of files.
    The zip object contains the ('BRnum', 'Pdf_URL', 'Report Html Address') columns
    """
    if not exists(excel_file):
        print(f'"{excel_file}" was not found!')
        exit(1)

    excel = pandas.read_excel(excel_file, sheet_name=0)
    num_cells = len(excel["BRnum"].values)

    report_names = zip(
        excel["BRnum"].values,
        excel["Pdf_URL"].values,
        excel["Report Html Address"].values,
    )
    return report_names, num_cells


async def download_file(session: aiohttp.ClientSession, tuple_data) -> str:
    """
    Tries to download a pdf file from the specified urls.
    """
    filename, link1, link2 = tuple_data
    outname = output_folder + filename + ".pdf"

    # Don't download existing reports
    if exists(outname):
        return ""  # f"0\t{filename}\n"

    # Empty cells become 'float', for some reason
    link1 = None if type(link1) is float else link1
    link2 = None if type(link2) is float else link2

    err = ""
    retries = dict()

    # Try links
    links = [link1, link2]
    while len(links) > 0:
        link: str = links.pop(0)
        if not link:
            continue

        if retries.get(link, 0) == max_retries:
            err = f"retries exhausted: {link}\n"
            continue

        # Ignore local files
        if link.startswith("file://"):
            continue

        # Fix html
        if link.startswith('<a href="'):
            link = link[len('<a href="') :]
            link = link[: link.find('"')]

        # Fix address starting with a dot
        if link[0] == ".":
            link = link[1:]

        # Patch incomplete urls
        url = urlparse(link)
        if len(url.scheme) == 0:
            # print("patching: ", link)
            # links.insert(0, "ftp://" + link)
            links.insert(0, "http://" + link)
            links.insert(0, "https://" + link)
            continue

        try:
            async with session.get(
                link,
                max_field_size=16 * 1024,  # 16k bytes response headers
                headers=headers,
                allow_redirects=True,
                chunked=True,
                timeout=aiohttp.ClientTimeout(
                    sock_connect=url_timeout, sock_read=url_timeout
                ),
                # raise_for_status=True,
            ) as response:
                accepted_content_types = [
                    "application/pdf",
                    "application/octet-stream",
                    "binary/octet-stream",
                ]

                if not response.content_type in accepted_content_types:
                    err = f"Link did not return a pdf for '{link}': {response.content_type}\n"
                    continue

                # if not response.content_length or response.content_length <= 8192:
                #    err = f"13\t{filename}\tbad sized pdf for '{link}': {response.content_length}\n"
                #    continue

                try:
                    with open(outname, "wb") as file:
                        # file.write((response.content_length * "X").encode())
                        async for chunk in response.content.iter_any():
                            file.write(chunk)

                    if os.path.getsize(outname) > 0:
                        err = ""
                        break
                    else:
                        os.remove(outname)
                        err = f"bad sized pdf\n"
                except aiohttp.http_exceptions.ContentLengthError as cle:
                    retries[link] = 1 + retries.get(link, 0)
                    links.insert(0, link)
                except Exception as e:
                    os.remove(outname)
                    err = f"file exception for '{link}' {e}\n"
                    break
        except TimeoutError as e:
            retries[link] = 1 + retries.get(link, 0)
            links.insert(0, link)
        except Exception as e:
            err = f"{type(e)} - '{e}': '{link}'\n"

    if 0 == len(err):
        return filename, None
    else:
        return filename, err


async def download_all_files():
    if not exists(output_folder):
        os.mkdir(output_folder)

    report_data, count = extract_report_names()

    session = aiohttp.ClientSession(
        cookie_jar=aiohttp.CookieJar(),
        connector=aiohttp.TCPConnector(ssl=False, limit=500),
        timeout=aiohttp.ClientTimeout(total=0),
    )

    good = []
    bad = []

    async with session:
        tasks = [download_file(session, tuple_data) for tuple_data in report_data]

        for f in tqdm(asyncio.as_completed(tasks), unit="pdf", total=count):
            try:
                filename, error = await f
                if not error:
                    good.append(filename)
                else:
                    bad.append(filename + "\t" + error)
            except Exception as e:
                bad.append("async io error\t" + str(e))

    with open("report.csv", "wt") as report:
        for file in good:
            report.write("0\t" + result)
        for error in bad:
            report.write("1\t" + error)


if __name__ == "__main__":
    asyncio.run(download_all_files())
