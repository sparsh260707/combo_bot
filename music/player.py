from pytgcalls.types.stream import AudioPiped
from .call import pytgcalls, queue

async def play_song(chat_id, file_path):
    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(file_path),
        stream_type="music"
    )
