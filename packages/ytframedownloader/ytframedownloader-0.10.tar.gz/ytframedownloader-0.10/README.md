### Download single frames from YT Videos

```python
from ytframedownloader import YT2Frames
#Will download https://yt-dl.org/latest/youtube-dl.exe and save it your cache folder.
#FFMPEG must be installed and in your path
ytf = (
    YT2Frames(
        youtubeurl="https://www.youtube.com/watch?v=UNTE7TXhv9c",
        foldertosave="f:\\testyoutubedownload",
        force_yt_downloader_update=False, #deletes youtube-dl.exe and downloads it again
    )
    .get_download_codes(desired_videoquality=640) #If the video quality is not available, will get the one that is closest
    .download_video()
    .convert_video_to_frames(fps=1) #One frame per second
)
```
