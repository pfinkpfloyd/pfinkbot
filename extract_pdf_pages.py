import pathlib
import sys
from os import path
from pathlib import Path, PurePath
from typing import Optional

import pymupdf as fitz
import requests
from urllib3.util import parse_url, Url

cache_dir = pathlib.Path("pdf_cache")
cache_dir.mkdir(parents=True, exist_ok=True)

def file_cache_path(name: str, file_name: str = "cache.pdf"):
    return Path(path.join(cache_dir, name, file_name))


def extract_single_page(doc, single_path_path: PurePath, pagenum: int):
    page = doc.load_page(pagenum)
    pixmap = page.get_pixmap(dpi=300)
    img = pixmap.tobytes()
    with open(single_path_path, 'wb') as file:
        file.write(img)


async def extract_pdf_page_range(url_path: str, start_page: Optional[int], end_page: Optional[int]):
    url = parse_url(url_path)

    doc, file_path = download_file_if_needed(url)
    ep = (doc.page_count - 1) if end_page is None else end_page
    file_refs= []
    for pagenum in range(start_page, ep + 1):
        page_path = file_path.parent.joinpath(f"{pagenum}.png")
        if not page_path.exists():
            extract_single_page(doc, page_path, pagenum - 1)
            print(f"Extracting pagenum: {pagenum}")
        file_refs.append(page_path)

    return file_refs

def download_file_if_needed(url: Url):

    file_name = path.basename(url.path)
    cache_dest = file_cache_path(file_name)
    cache_dest.parent.mkdir(parents=True, exist_ok=True)
    if not cache_dest.exists():
        response = requests.get(url)
        if response.status_code == 200:
            with open(cache_dest, 'wb') as file:
                file.write(response.content)
            print('File downloaded successfully')
        else:
            print('Failed to download file')
            raise Exception(f"Failed to download file: {url} {response.status_code}")
    else:
        print(f"{file_name} already downloaded")

    doc = fitz.open(cache_dest)
    return doc, cache_dest


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
