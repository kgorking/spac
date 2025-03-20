from genericpath import exists
import ssl
import urllib.parse
from aiohttp.client import ClientTimeout
import aiohttp.client_exceptions
from aiohttp.cookiejar import CookieJar
import pandas
import asyncio
import aiohttp
import os
import certifi
from tqdm import tqdm
from urllib.parse import urlparse

excel_file = "./data/GRI_2017_2020 (1).xlsx"
output_folder = "./download/"
max_retries = 3
url_timeout = 60.0

# Headers used to pretend we are a browser.
# Some sites reject requests if they do not look like
# they originate from a browser.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
    "Accept-encoding": "gzip, deflate, br, zstd",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
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

    rapport_names = zip(
        excel["BRnum"].values,
        excel["Pdf_URL"].values,
        excel["Report Html Address"].values,
    )
    return rapport_names, num_cells


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
            err = f"10\t{filename}\tretries exhausted: {link}\n"
            continue

        # Ignore local files
        if link.startswith("file://"):
            continue

        # Fix html
        if link.startswith('<a href="'):
            link = link[len('<a href="') :]
            link = link[: link.find('"')]

        # Fix unicode 'Full Stop'
        link = link.replace("\x2e", ".")

        # Patch incomplete urls
        url = urlparse(link)
        if len(url.scheme) == 0:
            # print("patching: ", link)
            links.insert(0, "ftp://" + link)
            links.insert(0, "http://" + link)
            links.insert(0, "https://" + link)
            continue

        try:
            async with session.get(
                link,
                headers=headers,
                allow_redirects=True,
                chunked=True,
                # chunked=False,
                # raise_for_status=True,
            ) as response:
                if not response.content_type in [
                    "application/pdf",
                    "application/octet-stream",
                ]:
                    err = f"12\t{filename}\tnot a pdf: {response.content_type}\n"
                    continue

                if response.content_length and response.content_length <= 8192:
                    err = f"13\t{filename}\tshit size pdf: {response.content_length}\n"
                    continue

                try:
                    with open(outname, "wb") as file:
                        # don't bother downloading the file, just fill it
                        # with junk, the same size as the actual pdf
                        file.write((response.content_length * "X").encode())
                        # file.write(response.content)
                    return f"0\t{filename}\n"
                except Exception as e:
                    os.remove(outname)
                    return f"X\t{filename}\tfile exception {e}\n"
        except aiohttp.InvalidURL as e:
            err = f"2\t{filename}\tinvalid url: '{e}'\n"
        except aiohttp.InvalidUrlClientError as e:
            err = f"3\t{filename}\tinvalid client url: '{e}'\n"
        except aiohttp.RedirectClientError as e:
            err = f"4\t{filename}\tredirect error: '{e}'\n"
        except aiohttp.InvalidUrlRedirectClientError as e:
            err = f"5\t{filename}\tmalformed url error: '{e}'\n"
        except aiohttp.NonHttpUrlClientError as e:
            err = f"6\t{filename}\tnon-http client error: '{e}'\n"
        except aiohttp.NonHttpUrlRedirectClientError as e:
            err = f"7\t{filename}\tnon-http client or redirect error: '{e}'\n"
        except aiohttp.ClientResponseError as e:
            err = f"8\t{filename}\t{e}\n"
        except aiohttp.ClientError as e:
            err = f"9\t{filename}\tclient error: {e}\n"
        except UnicodeEncodeError as e:
            err = f"12\t{filename}\tunicode error: {e}\n"
            pass
        except TimeoutError as e:
            retries[link] = 1 + retries.get(link, 0)
            links.insert(0, link)  #
        except Exception as e:
            err = f"11\t{filename}\tunknown error: {type(e)} - '{e}'\n"

    if 0 == len(err):
        return ""  # f"1\t{filename}"
    else:
        return err


async def download_all_files():
    if not exists(output_folder):
        os.mkdir(output_folder)

    report_data, count = extract_report_names()
    # report_data = [['test', 'https://www.bunge.com/sites/default/files/2018_gri_sustainability_report.pdf', None]]
    # count = 1

    ssl_ctx = ssl.create_default_context(cafile=certifi.where(), purpose=ssl.Purpose.SERVER_AUTH)
    connector = aiohttp.TCPConnector(ssl=ssl_ctx) #, timeout_ceil_threshold=url_timeout)#, limit=50)

    async with aiohttp.ClientSession(
        cookie_jar=CookieJar(),
        connector=connector,
        #timeout=ClientTimeout(total=url_timeout),
    ) as session:
        tasks = [download_file(session, tuple_data) for tuple_data in report_data]

        with open("report.csv", "wt") as report:
            for f in tqdm(
                asyncio.as_completed(tasks),
                desc="Henter pdf filer",
                unit=" pdf",
                total=count,
            ):
                try:
                    result = await f
                    report.write(result)
                except Exception as e:
                    report.write("X: {e}")


if __name__ == "__main__":
    asyncio.run(download_all_files())
