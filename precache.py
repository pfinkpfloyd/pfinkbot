import asyncio
import logging

from extract_pdf_pages import download_file_if_needed
from literature import literature_options, Literature

logger = logging.getLogger(__name__)


async def _preache_single_file(lit: Literature):
    try:
        doc, _, was_downloaded = await download_file_if_needed(lit.url)
        if not was_downloaded:
            logger.debug(f'{lit.name} [already cached]')
        else:
            logger.info(f'{lit.name} [downloaded]')
    except Exception as e:
        logger.info(f"{lit.name}: [failed to download/cache]: {e}")


# Precaches all literature without awaiting the coroutines
def precache_literature():
    tasks = []
    logger.info("Attempt to populate download cache")
    for lit in literature_options:
        tasks.append(_preache_single_file(lit))
    return asyncio.gather(*tasks)
