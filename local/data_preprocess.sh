#/bin/bash
rm -rf data/all

mkdir data/all
mkdir data/all/TAB

python3 local/rename_data.py /opt/TCC300/tcc300/ data/all/TAB

mkdir data/all/WAV

python3 local/rename_wav.py /opt/TCC300/tcc300/WAV data/all/WAV

rm data/all/TAB/F03110625_0.TAB
rm data/all/TAB/F03111360_0.TAB
rm data/all/TAB/F03112460_0.TAB
rm data/all/TAB/F03113560_0.TAB
rm data/all/TAB/F03114560_0.TAB
rm data/all/TAB/M03110360_0.TAB
rm data/all/TAB/M03111460_0.TAB
rm data/all/TAB/M03112460_0.TAB
rm data/all/TAB/M03113460_0.TAB
rm data/all/TAB/M03114460_0.TAB
