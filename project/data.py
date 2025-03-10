import json

def get_music(file_path:str = "music.json", music_id:int|None = None) -> list[dict]|dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        music = json.load(f)
        if not music_id is None and music_id < len(music):
            return music[music_id]
        return music


def get_guitar(file_path:str = "music.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        all_info = json.load(f)
        all_instruments = []
        for guitarist in all_info:
            for i in guitarist['instruments']:
                all_instruments.append(i)
        return all_instruments