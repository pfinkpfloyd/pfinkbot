import os
from typing import Optional

import certifi
from discord import Intents, app_commands, File, Interaction, InteractionResponse
from urllib3.util import parse_url

from client import PfinkBotClient
from extract_pdf_pages import extract_pdf_page_range, download_file_if_needed
from literature import literature_options, find_literature_by_url

os.environ["SSL_CERT_FILE"] = certifi.where()

PFINK_TEST_SERVER_ID = 1347378090501996636

intents = Intents.default()
# Allows us to read message content
intents.message_content = True
client = PfinkBotClient(intents=intents, guilds_to_sync=[PFINK_TEST_SERVER_ID])

# noinspection PyUnusedLocal
async def literature_options_autocomplete(
        interaction: Interaction,
        current: str,
) -> list[app_commands.Choice[str]]:
    values = [
        app_commands.Choice(name=lit.name, value=lit.url)
        for lit in literature_options if current.lower() in lit.name.lower()
    ]
    return values[:20]


@client.tree.command(description='Extracts pages from a literature pdf file')
@app_commands.describe(literature_name='Literature name or url')
@app_commands.describe(start_page='Starting page')
@app_commands.describe(end_page='Ending page')
@app_commands.autocomplete(literature_name=literature_options_autocomplete)
async def literature_pages(interaction: Interaction, literature_name: str, start_page: int, end_page: int):
    # noinspection PyTypeChecker
    resp: InteractionResponse = interaction.response
    lit = find_literature_by_url(literature_name)
    if start_page < 1:
        await resp.send_message(f'Hi, {interaction.user.mention}, starting page must be greater than 0')
    elif end_page < start_page:
        await resp.send_message(
            f'Hi, {interaction.user.mention}, starting page must be smaller than end page')
    elif (end_page - start_page) > 10:
        await resp.send_message(f'Hi, {interaction.user.mention}, You can extract only 10 pages')
    else:

        try:
            doc,_=download_file_if_needed(parse_url(lit.url))
            if doc.page_count < start_page:
                await resp.send_message(f"Page {start_page} does not exist in {lit.name} (max page: {doc.page_count})")
                return
            if doc.page_count < end_page:
                await resp.send_message(f"Page {end_page} does not exist in {lit.name} (max page: {doc.page_count})")
                return

            extracted_files = await extract_pdf_page_range(literature_name, start_page, end_page)
            files = [File(fp=file_path) for file_path in extracted_files]

            if len(files) > 0:
                msg=f'\n{lit.name}'
                if lit.url != lit.name:
                    msg+=f'\n{lit.url}'
                msg+=f'\nPages {start_page} to {end_page}'
                await resp.send_message(msg, files=files)
        except Exception as e:
            await resp.send_message(f"Error extracting PDF pages: {e}")
            return






client.run(os.environ['DISCORD_TOKEN'], reconnect=True)
