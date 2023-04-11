from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import ContentType

from cfg import settings
dp = settings()[2]
storage = settings()[0]

from handlers import users, states


@dp.message_handler(commands=['start'])
async def start_command(msg: Message):
    await users.start_command(msg)

@dp.callback_query_handler(text_contains="resourses")
async def resourses(call: CallbackQuery):
    await users.resurses(call)

@dp.callback_query_handler(text_contains="back_")
async def backer(call: CallbackQuery):
    await users.backer(call)

@dp.callback_query_handler(text_contains="addRes", state=None)
async def addRes(call: CallbackQuery, state: FSMContext):
    await users.addRes(call, state)

@dp.message_handler(content_types=ContentType.TEXT, state=states.addRess.st)
async def addCh2(msg: Message, state: FSMContext):
    await users.getCH(msg, state)

@dp.callback_query_handler(state=states.addRess.st)
async def cancel_addCH(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await users.backer(call)

@dp.callback_query_handler(text_contains="change_")
async def changeStatus(call: CallbackQuery):
    await users.change_status(call)

@dp.callback_query_handler(text_contains="delete_")
async def deleteChannel(call: CallbackQuery):
    await users.delete(call)

@dp.callback_query_handler(text_contains="settings")
async def settings(call: CallbackQuery):
    await users.settings(call)

@dp.callback_query_handler(text_contains="timeout_")
async def ch_settings(call: CallbackQuery):
    await users.ch_sett(call)

#########################################################################
@dp.callback_query_handler(text_contains="post", state=None)
async def posting(call: CallbackQuery, state: FSMContext):
    await users.posting(call, state)

@dp.callback_query_handler(text_contains="back_", state=states.post.msg0)
async def bm(call: CallbackQuery, state: FSMContext):
    await users.backer(call, state)

@dp.callback_query_handler(text_contains="get_saved", state=states.post.msg0)
async def get_saved(call: CallbackQuery, state: FSMContext):
    await users.get_saved(call, state)

@dp.callback_query_handler(state=states.post.msg0)
async def choosing(call: CallbackQuery, state: FSMContext):
    await users.choosing(call, state)

@dp.message_handler(content_types=ContentType.TEXT, state=states.post.text)
async def post_text(msg: Message, state: FSMContext):
    await users.post_text(msg, state)

@dp.message_handler(content_types=ContentType.TEXT, state=states.post.kb)
async def post_kb(msg: Message, state: FSMContext):
    await users.post_kb(msg, state)

@dp.message_handler(content_types=ContentType.PHOTO, state=states.post.media)
async def post_photo(msg: Message, state: FSMContext):
    await users.post_photo(msg, state)

@dp.message_handler(content_types=ContentType.VIDEO, state=states.post.media)
async def post_video(msg: Message, state: FSMContext):
    await users.post_video(msg, state)

@dp.message_handler(content_types=ContentType.VIDEO_NOTE, state=states.post.media)
async def post_note(msg: Message, state: FSMContext):
    await users.post_note(msg, state)

@dp.message_handler(content_types=ContentType.VOICE, state=states.post.media)
async def post_voice(msg: Message, state: FSMContext):
    await users.post_voice(msg, state)

@dp.message_handler(content_types=ContentType.AUDIO, state=states.post.media)
async def post_audio(msg: Message, state: FSMContext):
    await users.post_audio(msg, state)

@dp.message_handler(content_types=ContentType.DOCUMENT, state=states.post.media)
async def post_doc(msg: Message, state: FSMContext):
    await users.post_doc(msg, state)

@dp.message_handler(content_types=ContentType.STICKER, state=states.post.media)
async def post_sticker(msg: Message, state: FSMContext):
    await users.post_sticker(msg, state)

@dp.callback_query_handler(text_contains="back_", state=states.post.media)
async def bm(call: CallbackQuery, state: FSMContext):
    await users.backer(call, state)

@dp.callback_query_handler(text_contains="back_", state=states.post.text)
async def bm_t(call: CallbackQuery, state: FSMContext):
    await users.backer(call, state)

@dp.callback_query_handler(text_contains="back_", state=states.post.kb)
async def bm_kb(call: CallbackQuery, state: FSMContext):
    await users.backer(call, state)

@dp.callback_query_handler(text_contains="back_", state=states.post.settigs)
async def bm_s1(call: CallbackQuery, state: FSMContext):
    await users.backer(call, state)

@dp.callback_query_handler(text_contains="save", state=states.post.settigs)
async def save_post(call: CallbackQuery, state: FSMContext):
    await users.save_post(call, state)

@dp.callback_query_handler(text_contains="changeOrd", state=states.post.settigs)
async def changeOrd(call: CallbackQuery, state: FSMContext):
    await users.change_ord(call, state)

@dp.callback_query_handler(text_contains="sett", state=states.post.settigs)
async def changeOrd2(call: CallbackQuery, state: FSMContext):
    await users.change_ord2(call, state)

@dp.callback_query_handler(text_contains="post", state=states.post.settigs)
async def changeOrd2(call: CallbackQuery, state: FSMContext):
    await users.posting3(call, state)