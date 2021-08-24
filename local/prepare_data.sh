#!/usr/bin/env bash
# Copyright 2015-2016  Sarah Flora Juan
# Copyright 2016  Johns Hopkins University (Author: Yenda Trmal)
# Copyright 2018  Yuan-Fu Liao, National Taipei University of Technology
#                 AsusTek Computer Inc. (Author: Alex Hung)

# Apache 2.0

set -e -o pipefail

. ./path.sh
. parse_options.sh
export USER=root

# have to remove previous files to avoid filtering speakers according to cmvn.scp and feats.scp
rm -rf   data/all data/train data/test data/eval data/local/train
mkdir -p data/all data/train data/test data/eval data/local/train data/temp

local/data_preprocess.sh
python3 local/prepare_text_segment_lexicon.py data/all/TAB data/all || exit 1;
python3 local/parse_text2wavscp_with_segments.py data/all/text data/all || exit 1;
#python3 local/prepare_text_lexicon.py data/all/TAB data/all || exit 1;
#python3 local/parse_text2wavscp.py data/all/text data/all || exit 1;

# fix_data_dir.sh fixes common mistakes (unsorted entries in wav.scp,
# duplicate entries and so on). Also, it regenerates the spk2utt from
# utt2spk
utils/fix_data_dir.sh data/all

echo "Preparing train and temp data"
# test set: F0206 F0207 F0208 F0209 M0206 M0207 M0208 M0209 
grep -E "(F0210|M0210|F0105|M0105|M0104)" data/all/utt2spk | awk '{print $2}' > data/all/cv.spk
#grep -E "(F0102|M0102|F0103|M0103|F0104|M0104|F0105|M0105|F0207|M0207|F0208|M0208|F0209|M0209|F0210|M0210)" data/all/utt2spk | awk '{print $2}' > data/all/cv.spk
utils/subset_data_dir_tr_cv.sh --cv-spk-list data/all/cv.spk data/all data/train data/temp

echo "Preparing test and eval data"
# eval set:
grep -E "(F0210|M0210)" data/temp/utt2spk | awk '{print $2}' > data/temp/cv.spk
#grep -E "(F0102|M0102|F0103|M0103|F0104|M0104|F0105|M0105)" data/temp/utt2spk | awk '{print $2}' > data/temp/cv.spk
utils/subset_data_dir_tr_cv.sh --cv-spk-list data/temp/cv.spk data/temp data/test data/eval
rm -rf data/temp

# for LM training
echo "cp data/train/text data/local/train/text for language model training"
cat data/train/text | awk '{$1=""}1;' | awk '{$1=$1}1;' > data/local/train/text

echo "Data preparation completed."
exit 0;
