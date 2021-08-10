#!/bin/bash
set -eo pipefail
. ./cmd.sh

steps/make_mfcc_pitch.sh --cmd "$train_cmd" --nj 20 data/train exp/make_mfcc/train mfcc || exit 1;
steps/compute_cmvn_stats.sh data/train exp/make_mfcc/train mfcc || exit 1;
utils/fix_data_dir.sh data/train || exit 1;
