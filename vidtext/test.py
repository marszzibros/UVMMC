from vidtofrm import vidtofrm

if __name__ == "__main__":
    
    video_path = "/home/raymondlab/Downloads/test1.mp4"
    batch_size = 50
    
    vtf = vidtofrm(video_path, batch_size)
    vtf.extframes()
    vtf.make_vid("/home/raymondlab/Documents/UVMMC/remove_text_vid/test1_output.mp4")