import io
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, URLInputFile
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pytube import YouTube

# Bot token can be obtained via https://t.me/BotFather
TOKEN = '6994701946:AAHYaSSO8n3MHwacizISx4U5uy6l3GMfbA4'

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    ...


@dp.message(F.text.regexp(r'https://\D{0,}youtu\D{0,}'))
async def echo_handler(message: Message) -> None:
    yt_video = YouTube(message.text)

    videos = yt_video.streams.filter(file_extension='mp4', type='video', progressive=True).order_by('resolution')

    buttons = [[]]
    for vid in videos:
        buttons[-1].append(InlineKeyboardButton(text=vid.resolution, url=vid.url))
        if len(buttons[-1]) == 3:
            buttons.append([])
    keys = InlineKeyboardMarkup(inline_keyboard=buttons)

    cool_video = videos.get_highest_resolution()
    video_file_url = URLInputFile(cool_video.url, filename=f'{yt_video.title}.mp4')

    tumbai_file_url = URLInputFile(yt_video.thumbnail_url, filename=f'{yt_video.title}.jpg')

    try:
        await message.answer_video(video_file_url)
    except BaseException:
        await message.answer_photo(tumbai_file_url)

    await message.answer(
        f'{html.bold(yt_video.title)} - {yt_video.author}\n\n{yt_video.description}',
        disable_web_page_preview=True
    )
    await message.answer(
        'скачать видео',
        reply_markup=keys
    )


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())