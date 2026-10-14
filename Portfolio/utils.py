import os
import subprocess


def make_web_video(instance, field="video"):
    """Re-save an uploaded video as a standard web MP4 (H.264 video, AAC audio, fast start)."""
    f = getattr(instance, field)
    if not f:
        return False

    src = f.path
    base, ext = os.path.splitext(src)
    tmp = base + ".converted.mp4"

    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-ac", "2",
        "-movflags", "+faststart",
        tmp,
    ]
    try:
        subprocess.run(cmd, check=True, timeout=900,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (FileNotFoundError, subprocess.SubprocessError):
        if os.path.exists(tmp):
            os.remove(tmp)
        return False                        # ffmpeg missing or failed: keep the original file

    if ext.lower() == ".mp4":
        os.replace(tmp, src)                # same name, new contents
    else:
        os.remove(src)                      # e.g. a .mov: remove it and keep the .mp4
        os.replace(tmp, base + ".mp4")
        f.name = os.path.splitext(f.name)[0] + ".mp4"
        instance.save(update_fields=[field])
    return True