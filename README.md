# Kaldi_ASR_TCC300
Kaldi_ASR_TCC300 is an ASR system trained on TCC300

Training recipe is mainly based on Kaldi Formosa project (kaldi/egs/formosa)

Write some python scripts to generate the demanding files for training

(see https://hackmd.io/hSqBEALiRkqqTD1djdWWzQ?view)
## Clone the project
please clone under the Kaldi relative file path because the two directories, steps and utils, symbolic link relatively to kaldi/egs/yesno
```sh
clone at kaldi/egs/anyname/
```
## Start Training
1. fix file name errors in TCC300 corpus

    Some file name errors might happened in TCC300.
    Check INSTRUCTIONS directory in TCC300 for the correct format
```sh
TAB file format F010101_0.TAB : X_XX_XX_XX_0.TAB Gender_School_Speaker_Utterance_0.TAB

WAV file formate F010101_0.WAV : X_XX_XX_XX_0.WAV Gender_School_Speaker_Utterance_0.WAV
```
3. change TCC corpus file path to local path in local/data_preprocess.sh

```sh
python3 local/rename_data.py /opt/TCC300/tcc300/ data/all/TAB -> 
python3 local/rename_data.py $(tcc_path) data/all/TAB
```
```sh
python3 local/rename_wav.py /opt/TCC300/tcc300/WAV data/all/WAV -> 
python3 local/rename_wav.py $(tcc_path) data/all/WAV
```
3. change pinyin and hanyu filepath to local path in prepare_text_segment_lexicon.py

```python
with open("/opt/asraData/chinese/pinyinTable.txt", 'r', encoding="big5") -> 
with open($(pinyinTable_path), 'r', encoding="big5")
```
```python
with open("/opt/asraData/chinese/hanyu.monophone.pam", 'r', encoding="utf-8") -> 
with open($(hanyu.monophone.pam_path), 'r', encoding="utf-8")
```
4. ./run.sh
