#!/bin/bash
#BSUB -n 16
#BSUB -R gpu
#BSUB -q "standard"
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -x
cd KerasSeq/seq2seq/
export VOCAB_SOURCE=~/KerasSeq/120Char_seq2seq/FullIntputvocab1
export VOCAB_TARGET=~/KerasSeq/120Char_seq2seq/FullOutputvocab1
export TRAIN_SOURCES=~/KerasSeq/120Char_seq2seq/Train_Fullinput120
export TRAIN_TARGETS=~/KerasSeq/120Char_seq2seq/Train_Fulloutput120
export DEV_SOURCES=~/KerasSeq/120Char_seq2seq/Test_Fullinput120
export DEV_TARGETS=~/KerasSeq/120Char_seq2seq/Test_Fulloutput120
export DEV_TARGETS_REF=~/KerasSeq/120Char_seq2seq/Test_Fulloutput120
export TRAIN_STEPS=200000
export MODEL_DIR=~/KerasSeq/120Char_seq2seq/Results/
mkdir -p $MODEL_DIR
python3.4 -m bin.train \
--config_paths="
       ./example_configs/BTS_80_rep.yml,
       ./example_configs/train_seq2seq.yml" \
   --model_params "
       vocab_source: $VOCAB_SOURCE
       vocab_target: $VOCAB_TARGET" \
   --input_pipeline_train "
     class: ParallelTextInputPipeline
     params:
       source_files:
         - $TRAIN_SOURCES
       target_files:
         - $TRAIN_TARGETS" \
   --input_pipeline_dev "
     class: ParallelTextInputPipeline
     params:
        source_files:
         - $DEV_SOURCES
        target_files:
         - $DEV_TARGETS" \
   --batch_size 32 \
   --train_steps $TRAIN_STEPS \
   --output_dir $MODEL_DIR
export PRED_DIR=${MODEL_DIR}/pred
mkdir -p ${PRED_DIR}
python3.4 -m bin.infer \
   --tasks "
     - class: DecodeText" \
   --model_dir $MODEL_DIR \
   --input_pipeline "
     class: ParallelTextInputPipeline
     params:
       source_files:
         - $DEV_SOURCES" \
   >  ${PRED_DIR}/predictions.txt
