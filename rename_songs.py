import os
import shutil
import sys

def rename_files(in_path, out_path):
    file_names = os.listdir(in_path)
    file_names = [x for x in file_names if x.endswith(".mp3")]
    for i, f in enumerate(file_names):
        f_orig = f
        f = f.replace(" (Official Video)", "").replace(" (Official Music Video)", "").replace(" (Video)", "")
        f = f.replace(" (OFFICIAL MUSIC VIDEO)", "").replace(" (Video Version)", "").replace("[OFFICIAL MUSIC VIDEO]", "")
        f = f.replace(" (HQ sound)", "").replace("..", ".").replace("├ë", "E").replace("ÔÇÄ", "")
        patterns = [" (Music Video)", " (Official Audio)", " (Vinyl)", " (Remastered)", " - official video", " (lyrics)",
                        " - Official Music Video", " (audio)", " (Shortened Version)", " (Single Version)", " (Part 2) (HQ)",
                        " [Official video]", " HQ", " (Version 2)", " [Official Music Video]", " [Official Video]"]
        for pattern in patterns:
            f = f.replace(pattern, "")

        shutil.copy(os.path.join(in_path, f_orig), os.path.join(out_path, f))
        

if __name__ == "__main__":
    dir_path = sys.argv[1]
    out_path = sys.argv[2]
    rename_files(dir_path, out_path)