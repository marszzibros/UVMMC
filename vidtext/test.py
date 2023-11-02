from vidtofrm import vidtofrm 
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Enter input file path",required=True)
    parser.add_argument('-b', '--batch', help="Enter batch size", default=5, type=int)
    parser.add_argument('-e','--every', help="Enter how many frames to skip", default=2, type=int)
    parser.add_argument('-g','--gpu', help="Enter the GPU status (True/False)", default=False, type=bool)
    parser.add_argument('-o','--output', help="Enter output file path",required=True)

    # Perform action
    args = parser.parse_args()

    # initialization
    """
    video_path  : specifying video path
    batch_size  : every batch_size, the OCR will detect the text; 
        (high batch_size will cause the lower accuracy, and vice versa)

    every       : specify how many frames you want to skip 
        (may lower the fps (frame rate) but increase the speed of the process)

    gpu         : using GPU will increase the speed dramatically
    """
    vid = vidtofrm(args.input, args.batch, args.every, args.gpu)

    # start processing
    vid.extframes()

    # make a video
    vid.make_vid(args.output)

if __name__ == '__main__':
    main ()