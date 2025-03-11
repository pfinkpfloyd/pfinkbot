import logging
import pathlib
import sys
from os import path
from pathlib import Path, PurePath
from typing import Optional

import pymupdf as fitz
import requests
from urllib3.util import parse_url, Url

logger = logging.getLogger(__name__)

# Downloaded literature files are placed in pdf_cache directory
cache_dir = pathlib.Path("pdf_cache")
cache_dir.mkdir(parents=True, exist_ok=True)

def file_cache_path(name: str, file_name: str = "cache.pdf"):
    """
     Calculates the expected location of the cached download file, based on the name of the file

     :param name: The name of the IP, used to create a subdirectory in the cache directory
     :param file_name: The name of the file within the subdirectory, defaults to "cache.pdf", which is the entire pdf
     :return: Path object representing the expected location of the file
     """
    return Path(path.join(cache_dir, name, file_name))

def extract_single_page(doc, single_path_path: PurePath, pagenum: int):
    """
    Extracts a single page from the pdf document, writing the page as a PNG to the specified path

    :param doc: A PyMuPDF document object
    :param single_path_path: Where to write the file
    :param pagenum: The page number to extract (1 is the first page)
    :return: None
    """
    page = doc.load_page(pagenum)
    pixmap = page.get_pixmap(dpi=300)
    img = pixmap.tobytes()
    with open(single_path_path, 'wb') as file:
        file.write(img)


async def extract_pdf_page_range(pdf_url: str, start_page: Optional[int], end_page: Optional[int]):
    """
    Extracts a range of pages from a pdf file, returning a list of file paths to the extracted pages

    :param pdf_url: URL to the pdf file
    :param start_page: The first page to extract (1 is the first page)
    :param end_page: The last page to extract, or None to extract to the end of document
    :return: List of file paths to the extracted pages
    """
    url = parse_url(pdf_url)

    doc, file_path = download_file_if_needed(url)
    ep = (doc.page_count - 1) if end_page is None else end_page
    file_refs= []
    for pagenum in range(start_page, ep + 1):
        page_path = file_path.parent.joinpath(f"{pagenum}.png")
        if not page_path.exists():
            extract_single_page(doc, page_path, pagenum - 1)
            logger.info(f"Extracting pagenum: {pagenum}")
        file_refs.append(page_path)

    return file_refs

def download_file_if_needed(url: Url):
    """
    Downloads a PDF file to a local cache, if it doesn't already exist.  Also parses the file into a PyMuPDF document object
    :param url:
    :return: Tuple of the PyMuPDF document object and the path to the downloaded file
    """
    file_name = path.basename(url.path)
    pdf_cache_dest = file_cache_path(file_name)

    # Create a folder to contain the cached PDF and extracted pages
    pdf_cache_dest.parent.mkdir(parents=True, exist_ok=True)

    if not pdf_cache_dest.exists():
        response = requests.get(url)
        if response.status_code == 200:
            with open(pdf_cache_dest, 'wb') as file:
                file.write(response.content)
            logger.debug(f'File downloaded successfully {url}')
        else:
            logger.warning(f'Failed to download file: {url} {response.status_code}')
            raise Exception(f"Failed to download file: {url} {response.status_code}")
    else:
        logger.debug(f"{file_name} already downloaded")

    doc = fitz.open(pdf_cache_dest)
    return doc, pdf_cache_dest

# Usage: python extract_pdf_pages.py <url> <start_page> <end_page>
if __name__ == '__main__':
    if len(sys.argv) > 1:
        url_arg = sys.argv[1]
        start_page_arg = 1
        end_page_arg = None

        if len(sys.argv) > 2:
            start_page_arg = int(sys.argv[2])
            if len(sys.argv) > 3:
                end_page_arg = int(sys.argv[3])

        extract_pdf_page_range(url_arg, start_page_arg, end_page_arg)
    else:
        print("Missing argument: URL to pdf file")
