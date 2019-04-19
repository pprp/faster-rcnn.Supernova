#!/usr/bin/env bash

CUDA_PATH=/usr/local/cuda-8.0/

cd src/cuda

echo "Compiling roi align kernels by nvcc..."
nvcc -c -o roi_align_kernel.cu.o roi_align_kernel.cu \
	 -D GOOGLE_CUDA=1 -x cu -Xcompiler -fPIC -arch=sm_52

cd ../../
python build.py
