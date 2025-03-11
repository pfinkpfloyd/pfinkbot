import logging
import os
import traceback

from discord import Intents, app_commands, File, Interaction, InteractionResponse
from discord.app_commands import Choice
from urllib3.util import parse_url

from client import PfinkBotClient
from extract_pdf_pages import extract_pdf_page_range, download_file_if_needed
from literature import literature_options, find_literature_by_url, Literature

logger = logging.getLogger(__name__)

intents = Intents.default()
# Allows us to read message content
intents.message_content = True
client = PfinkBotClient(intents=intents, guilds_to_sync=[
    1347378090501996636, #Pfink's Test Server
    # Add more guilds here if you want to sync commands with them
])

# noinspection PyUnusedLocal
async def literature_options_autocomplete(
        interaction: Interaction,
        current: str,
) -> list[Choice[str]]:
    """
    Handles autocomplete for literature options based on input
    :param interaction:
    :param current: The typed text provided by the user
    :return:
    """

    current = "" if current is None else current.strip()
    values = [
        Choice(name=lit.name, value=lit.url)
        for lit in literature_options if current.lower() in lit.name.lower()
    ]

    # Discord limits number of autocomplete responses
    return values[:20]


def validate_input(lit: Literature, start_page: int, end_page: int) -> list[str]:
    literature_name = lit.name

    errors = []
    if literature_name is None or literature_name.strip() == "":
        errors.append('please provide a literature name or url')

    result = parse_url(lit.url.strip())
    if not all([result.scheme, result.netloc]):
        errors.append(f'oopsies!  We couldn\'t download the file **{lit.url}**. <-- If that seems weird, you probably need to click on the Literature name in the drop down after searching. Sometimes it takes a second.')
    if start_page < 1:
        errors.append('starting page must be at least 1')
    elif end_page < start_page:
        errors.append('starting page must be smaller than end page (that one\'s on you)')
    if (end_page - start_page) > 10:
        errors.append('you can extract only 10 pages.  We only have 23 internet credits left for the month.')
    return errors


def validate_doc(lit, doc, start_page: int, end_page: int) -> list[str]:
    errors = []
    if doc.page_count < start_page:
        errors.append(f"Page {start_page} does not exist in {lit.name} (max page: {doc.page_count})")

    if doc.page_count < end_page:
        errors.append(f"Page {end_page} does not exist in {lit.name} (max page: {doc.page_count})")

    return errors

async def send_errors(interaction:Interaction, resp:InteractionResponse, err:list[str], message:str='Bless all our hearts, we couldn\'t make that work.  Here are some tips:'):
    msg=f'Hi, {interaction.user.mention}: {message}'
    if len(err) > 0:
        msg+="\n"
        for e in err:
            msg += f' - {e}\n'
    await resp.send_message(msg)

@client.tree.command(description='Extracts pages from a literature pdf file')
@app_commands.describe(literature_name='Literature name or url')
@app_commands.describe(start_page='Starting page')
@app_commands.describe(end_page='Ending page')
@app_commands.autocomplete(literature_name=literature_options_autocomplete)
async def literature_pages(interaction: Interaction, literature_name: str, start_page: int, end_page: int):
    # noinspection PyTypeChecker
    resp: InteractionResponse = interaction.response

    lit = find_literature_by_url(literature_name)
    errors = validate_input(lit, start_page, end_page)
    if len(errors) > 0:
        return await send_errors(interaction, resp, errors)

    try:
        doc, _ = download_file_if_needed(parse_url(lit.url))
        errors = validate_doc(lit, doc, start_page, end_page)
        if len(errors) > 0:
            return await send_errors(interaction, resp, errors)

        extracted_files = await extract_pdf_page_range(literature_name, start_page, end_page)
        files = [File(fp=file_path) for file_path in extracted_files]

        if len(files) > 0:
            msg = f'\n{lit.name}'
            if lit.url != lit.name:
                msg += f'\n{lit.url}'
            msg += f'\nPDF Pages {start_page} to {end_page}'
            await resp.send_message(msg, files=files)
    except Exception as e:
        logger.exception("Error extracting PDF pages: %e", e, exc_info=True)
        traceback.print_exc()
        await send_errors(interaction, resp, [], f"Shit blew up. We\'re sorry. Try again, maybe it will work, maybe it won\'t")
        await resp.send_message(f"Error extracting PDF pages: {e}")


client.run(os.environ['DISCORD_TOKEN'], reconnect=True)
