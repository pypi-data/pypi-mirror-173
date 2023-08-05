import os
import subprocess
from pathlib import Path
import pandas as pd
import regex
import requests
from appdirs import user_cache_dir
from a_pandas_ex_closest_neighbours import find_neighbours

CACHE_DIR = Path(user_cache_dir("ytdownloader"))
http_exefile = "https://yt-dl.org/latest/youtube-dl.exe"
youtubedownloaderonhdd = os.path.join(CACHE_DIR, "youtube-dl.exe")


def _save_cache(cache_file: str, data) -> None:
    try:
        if not CACHE_DIR.exists():
            CACHE_DIR.mkdir(parents=True)

        with open(cache_file, mode="wb") as f:
            f.write(data)

    except OSError:
        pass


def download_yt_downloader(force_download):
    if force_download:
        if os.path.exists(youtubedownloaderonhdd):
            try:
                os.remove(youtubedownloaderonhdd)
            except Exception:
                pass
    if not os.path.exists(youtubedownloaderonhdd):
        with requests.get(http_exefile) as req:
            _save_cache(youtubedownloaderonhdd, req.content)


def get_youtube_id(youtubeurl):
    ytid = youtubeurl[-11:]
    return ytid


def get_hdd_link(folder_path, ytid):
    youtubevideolink = os.path.join(folder_path, ytid, ytid + ".mp4")
    youtubeaudionhdd = os.path.join(folder_path, ytid, ytid + ".mp3")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    foldertosave_frames = os.path.join(folder_path, ytid, "frames")
    if not os.path.exists(foldertosave_frames):
        os.makedirs(foldertosave_frames)
    return youtubevideolink, foldertosave_frames, youtubeaudionhdd


def get_df_all_resolutions(youtubedownloaderonhdd, youtubeurl):
    proc = subprocess.run(
        [youtubedownloaderonhdd, "-v", "-F", youtubeurl],
        shell=False,
        capture_output=True,
    )
    df = pd.DataFrame(
        [
            x.split(maxsplit=5)
            for x in proc.stdout.decode("utf-8", "ignore").splitlines()
            if regex.search(r"^\d", x) is not None
        ]
    )
    allaudios = df.loc[
        (df[2].str.contains("audio") & df[3].str.contains("only"))
    ].copy()
    allaudios[3] = allaudios[5].str.replace(
        r"^(\d+)[^\d]*\s+,\s+.*", r"\g<1>", regex=True
    )
    allaudios[3] = allaudios[3].astype(int)

    df = df.loc[~(df[2].str.contains("audio") & df[3].str.contains("only"))]
    df[5] = df[5].str.replace(r"^\s*,\s*", "", regex=True)
    df[3] = df[3].str.replace(r"[^\d]+", "", regex=True)
    df[3] = df[3].astype(int)
    return df, allaudios


def get_code_for_desired_resolution(
    df=None,
    resolution=640,
    get_higher_no_results=True,
    youtubedownloaderonhdd=None,
    youtubeurl=None,
    audio_or_video="video",
):
    allaudios = pd.DataFrame()
    if df is None:
        df, allaudios = get_df_all_resolutions(youtubedownloaderonhdd, youtubeurl)
    if audio_or_video == "audio":
        df = allaudios.copy()
    min_neighbours2, max_neighbours2 = find_neighbours(
        series=df[3], value=resolution, convertdtypes=False, accept_exact_match=True
    )
    if get_higher_no_results:
        if not max_neighbours2.empty:
            resdo = df.loc[max_neighbours2.upper_index.iloc[0]].iloc[0]
        else:
            resdo = df.loc[min_neighbours2.lower_index.iloc[0]].iloc[0]

    else:
        if not min_neighbours2.empty:
            resdo = df.loc[min_neighbours2.lower_index.iloc[0]].iloc[0]
        else:
            resdo = df.loc[max_neighbours2.upper_index.iloc[0]].iloc[0]

    return resdo


class YT2Frames:
    def __init__(
        self,
        youtubeurl: str,
        foldertosave: str,
        force_yt_downloader_update: bool = False,
    ):
        download_yt_downloader(force_download=force_yt_downloader_update)
        self.youtubeurl = youtubeurl
        self.foldertosave = foldertosave
        self.ytid = get_youtube_id(youtubeurl)
        (
            self.youtubevideonhdd,
            self.single_image_folder,
            self.youtubeaudionhdd,
        ) = get_hdd_link(foldertosave, ytid=self.ytid)
        self.df = pd.DataFrame()
        self.dfaudio = pd.DataFrame()
        self.video_download_code = None
        self.audio_download_code = None

    def get_download_codes(
        self, desired_videoquality: int = 640, desired_audioquality: int = 128
    ):
        df, dfaudio = get_df_all_resolutions(youtubedownloaderonhdd, self.youtubeurl)
        self.df = df.copy()
        self.dfaudio = dfaudio.copy()

        min_neighboursdf, max_neighboursdf = find_neighbours(
            series=df[3],
            value=desired_videoquality,
            convertdtypes=False,
            accept_exact_match=True,
        )

        if not max_neighboursdf.empty:
            resultsvid = df.iloc[max_neighboursdf.upper_index.iloc[0]][0]
        else:
            resultsvid = df.iloc[min_neighboursdf.lower_index.iloc[0]][0]

        min_neighboursdfaudio, max_neighboursdfaudio = find_neighbours(
            series=dfaudio[3],
            value=desired_audioquality,
            convertdtypes=False,
            accept_exact_match=True,
        )

        if not max_neighboursdfaudio.empty:
            resultsaudio = df.iloc[max_neighboursdfaudio.upper_index.iloc[0]][0]
        else:
            resultsaudio = df.iloc[min_neighboursdfaudio.lower_index.iloc[0]][0]
        self.video_download_code = resultsvid
        self.audio_download_code = resultsaudio
        return self

    def download_audio(self):
        procdown = subprocess.run(
            [
                youtubedownloaderonhdd,
                "-o",
                self.youtubeaudionhdd,
                "-v",
                "-f",
                self.audio_download_code,
                self.youtubeurl,
            ],
            capture_output=False,
        )
        return self

    def download_video(self):
        procdown = subprocess.run(
            [
                youtubedownloaderonhdd,
                "-o",
                self.youtubevideonhdd,
                "-v",
                "-f",
                self.video_download_code,
                self.youtubeurl,
            ],
            capture_output=False,
        )
        return self

    def convert_video_to_frames(self, fps: int = 1):
        procdown = subprocess.run(
            [
                "ffmpeg",
                "-i",
                self.youtubevideonhdd,
                "-vf",
                f"fps={fps}",
                f"{self.single_image_folder}{os.sep}out%d.png",
            ],
            capture_output=False,
        )
        return self


# from z_get_yt_downloader import YT2Frames
# #Will download https://yt-dl.org/latest/youtube-dl.exe and save it your cache folder.
# #FFMPEG must be installed and in your path
# ytf = (
#     YT2Frames(
#         youtubeurl="https://www.youtube.com/watch?v=UNTE7TXhv9c",
#         foldertosave="f:\\testyoutubedownload",
#         force_yt_downloader_update=False, #deletes youtube-dl.exe and downloads it again
#     )
#     .get_download_codes(desired_videoquality=640) #If the video quality is not available, will the one that is closest
#     .download_video()
#     .convert_video_to_frames(fps=1) #One frame per second
# )
