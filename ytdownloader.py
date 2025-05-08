import os
import json
import shutil
import yt_dlp

def load_config():
    config_path = "config.json"
    if not os.path.exists(config_path):
        print("Arquivo de configuração não encontrado! Crie um config.json.")
        exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def choose_format():
    print("Escolha o formato de áudio para baixar:")
    print("1 - mp3")
    print("2 - ogg")
    print("3 - m4a")
    print("4 - wav")
    choice = input("Digite o número do formato desejado: ").strip()
    formats = {"1": "mp3", "2": "ogg", "3": "m4a", "4": "wav"}
    return formats.get(choice, "mp3")

def check_ffmpeg(audio_format):
    # m4a geralmente não precisa de ffmpeg, outros sim
    if audio_format not in ["m4a"]:
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path is None:
            print("\nATENÇÃO: Para baixar em formato", audio_format.upper(), "é necessário ter o ffmpeg instalado no sistema.")
            print("Baixe em: https://ffmpeg.org/download.html")
            print("Ou escolha o formato m4a, que não exige ffmpeg.\n")
            exit(1)

def download_audio(url, download_path, audio_format):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'noplaylist': False,
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': '192',
        }],
        'progress_hooks': [download_hook],
    }

    print("Iniciando download...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("Download concluído!")
        except Exception as e:
            print(f"Erro ao baixar: {e}")

def download_hook(d):
    if d['status'] == 'finished':
        print('Download finalizado, convertendo...')
    elif d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        print(f"Baixando: {percent}", end='\r')

def main():
    config = load_config()
    download_path = config.get("download_path", "./musicas_baixadas")
    os.makedirs(download_path, exist_ok=True)

    print("=== SCRIPT_NZA YTDownloader ===")
    url = input("Cole o link da música ou playlist do YouTube: ").strip()
    audio_format = choose_format()
    check_ffmpeg(audio_format)
    print(f"Baixando para: {download_path} no formato: {audio_format}")

    download_audio(url, download_path, audio_format)

if __name__ == "__main__":
    main()