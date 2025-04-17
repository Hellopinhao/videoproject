import os
path = "/Users/charleslee/Downloads/Videos 30s"
folders = [f for f in os.listdir(path) if not f.startswith('.')]
for f in folders:
    cate = os.path.join(path,f)
    files = [fd for fd in os.listdir(cate) if not fd.startswith('.')]
    f_lower = f.lower()
    for i, v in enumerate(files):
        video = os.path.join(cate, v)
        os.rename(video, os.path.join(cate,f_lower+str(i+1)+".mp4"))