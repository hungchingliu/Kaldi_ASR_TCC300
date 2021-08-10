import os
import sys


def create_utt2spk(path, target):
    with open (os.path.join(target, "utt2spk"), 'w', encoding="utf-8") as utt2spk, \
    open (path, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            utt_id = line.split()[0]
            utt2spk.write(utt_id + " " + utt_id[0:7] + "\n")


def create_wavscp(path, target):
    with open(os.path.join(target, "wav.scp"), 'w', encoding="utf-8") as scp, \
    open (path, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            utt_id = line.split()[0]
            file_id = utt_id[:-3]
            file_path = os.path.join("/opt/kaldi/egs/tcc300/s0/data/all/WAV/", file_id + ".wav")
            scp.write(file_id + " " + file_path + "\n")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        path, target = sys.argv[1], sys.argv[2]
        create_utt2spk(path, target)
        create_wavscp(path, target)
