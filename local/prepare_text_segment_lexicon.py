# -*- coding: utf-8 -*-
import jieba
import os
import sys
stopwords = ["，", "。", "、", "？", "：", "；", "「", "」", "！", "˙", "（", "）", "˙", "．", "•",\
             "《", "》", "︰", "Ｘ", "－"]
chinese_tones = ["ˇ", "ˋ", "ˊ", "˙"]

def frame_to_time(frame):
    if frame == 0:
        return 0
    else:
        return (frame * 10 + 20) / 1000.0

def load_pinyin_table():

    pinyin_table = dict()
    with open("/opt/asraData/chinese/pinyinTable.txt", 'r', encoding="big5") as pinyin_file:
        lines = pinyin_file.readlines()
        for line in lines:
            _, _, pinyin, hanyu = line.split()
            pinyin_table[pinyin] = hanyu
    return pinyin_table

def load_hanyu_table():

    hanyu_table = dict()
    with open("/opt/asraData/chinese/hanyu.monophone.pam", 'r', encoding="utf-8") as hanyu_file:
        lines = hanyu_file.readlines()
        for line in lines:
            hanyu, phonemes = line.split()
            hanyu_table[hanyu] = phonemes

    return hanyu_table

def pinyin2phonemes(word_pinyin):
    word_phonemes = ""
    flag = True
    for pinyin in word_pinyin:
        if pinyin[-1] in chinese_tones:
            pinyin = pinyin[0:-1]
        phone = hanyu_table[pinyin_table[pinyin]].split("-")
        phonemes = " ".join(phone)
        if flag:
            word_phonemes = phonemes
            flag = False
        else:
            word_phonemes = word_phonemes + " " + phonemes

    return word_phonemes

def parse_TAB(file, path, out_path):

    path = os.path.join(path, file)
    with open(os.path.join(out_path, "text"), 'a', encoding="utf-8") as text, \
    open(os.path.join(out_path, "segments"), 'a', encoding="utf-8") as segment, \
    open(path, 'r', encoding="big5") as f:

        first_line = f.readline()
        _, file_id, sentence_num = first_line.split()


        for i in range(int(sentence_num)):
            info = f.readline().split()
            sentence = f.readline()
            _ = f.readline()
            pinyin = f.readline()

            for stopword in stopwords:
                sentence = sentence.replace(stopword, "")
                sentence = sentence.replace(" ", "")
                pinyin = pinyin.replace(stopword, "")

            word_list = jieba.cut(sentence)
            sentence = " ".join(word_list)
            words = sentence.split()
            pinyins = pinyin.split()

            pinyin_index = 0
            for word in words:
                alphabet_num = len(word)
                word_pinyin = pinyins[pinyin_index:pinyin_index + alphabet_num]
                pinyin_index += alphabet_num
                word_phonemes = pinyin2phonemes(word_pinyin)
                lexicon[word] = word_phonemes


            text.write(file[:-4] + "_" + "{:0>2d}".format(i))
            text.write(" " + sentence)

            segment.write(file[:-4] + "_" + "{:0>2d}".format(i))
            segment.write(" " + file[:-4])

            start_frame, frame_length = int(info[1]), int(info[2])
            end_frame = start_frame + frame_length
            start_time = frame_to_time(start_frame) 
            end_time = frame_to_time(end_frame)
            if start_time > 0.05:
                start_time -= 0.05
            if i != int(sentence_num) - 1:
                end_time += 0.05
            segment.write(" " + str(round(start_time, 2)) + " "+  str(round(end_time, 2)) + "\n")

def main():

    if len(sys.argv) == 3:
        path = sys.argv[1]
        out_path = sys.argv[2]
        for file in os.listdir(path):
            if file[-4:] == ".TAB":
#                print(file)
                parse_TAB(file, path, out_path)
        with open(os.path.join(out_path, "lexicon.txt"), "w", encoding="utf-8") as l, \
        open(os.path.join(out_path, "words"), "w", encoding="utf-8") as w:
            for word, phonemes in lexicon.items():
                w.write(word + "\n")
                l.write(word + " " + phonemes + "\n")

if __name__  == "__main__":
    hanyu_table = load_hanyu_table()
    pinyin_table = load_pinyin_table()
    lexicon = dict();
    main()
