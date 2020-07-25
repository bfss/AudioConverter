import subprocess
import os
from pathlib import Path

def mp32wav(src, dst):
    conversion_command = [
        'ffmpeg',
        '-y',
        "-f", 
        "mp3", 
        "-i", src,
        "-acodec", "pcm_s16le",
        "-ac", "1",
        "-ar", "16000",
        dst
    ]
    cmd = "ffmpeg -y -f mp3 -i " + src + " -acodec pcm_s16le -ac 1 -ar 16000 " + dst
    
    s = subprocess.Popen(conversion_command,shell=True)
    s.wait()