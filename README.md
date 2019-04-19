# Faster R-CNN supernova

## 说明

本项目基于faster-rcnn.pytorch进行修改，主要用于参加2019年未来杯挑战赛图像组比赛，比赛目标是识别超新星，比赛网址 [https://ai.futurelab.tv/](https://ai.futurelab.tv/)

比赛**最终方案**：Faster R-CNN + ResNet101 + Anchor Scale(1,2,3) + 数据集(中心切割，扩充，放大) ， 

最终得分：0.740527 ，西北区第三名

与原项目相比主要添加了**以下改进**：

- 添加了demo_split.py, 提供了将图片均等切割为四部分，然后放大为原来的二倍，然后进行检测，通过nms挑前三个得分最高的框。
- 添加了score.py，专门用于程序离线跑分，通过计算submit.csv和list.csv进行一个结果的计算。
- 添加了模型对densenet系列的支持
- preprocess文件夹中提供了一系列数据处理，可视化等python程序

## 环境搭建:

>```
>conda create -n pytorch python=3.6
>conda install pytorch torchvision cudatoolkit=9.0 -c pytorch=0.4.0
>pip install -r requirements.txt
>cd lib
>sh make.sh
>```

在data/pretrained_model文件夹下运行命令(下载预训练权重):

```
wget https://filebox.ece.vt.edu/~jw2yang/faster-rcnn/pretrained-base-models/res101_caffe.pth
```

将训练得到的模型`faster_rcnn_1_1_2514.pth`放在:`StarFRCNN/models/res101/pascal_voc`目录下

## 数据预处理：

说明:训练数据与测试数据都需要进行以下步骤的预处理．

### **训练集**: 

1. af2019-cv-training-20190312文件夹放置在preprocess文件夹下,运行`python merge3to1_train.py`

即可得到`merged_train`文件夹.

2. 制作以下形式的VOC数据集.

```
VOCdevkit2007
        - VOC2007
            - Annotations (标签XML文件，用对应的图片处理工具人工生成的)
            - ImageSets (生成的方法是用sh或者MATLAB语言生成)
                - Main
                    - test.txt
                    - train.txt
                    - trainval.txt
                    - val.txt
            - JPEGImages(原始图片)
```

3. merged_train文件夹下的图片放置到JPEGImages

4. 在preprocess目录下创建xml目录,```mkdir xml```(用于保存xml文件)

5. 在preprocess目录下创建error.txt ```touch error.txt```(用于记录标注出错的文件)

6. 运行`python generateXmlFromCsv.py`得到xml文件夹中的xml文件,将其放到Annotations文件夹.

7. 将preprocess文件夹下的`generate4Txt.py`放到VOC2007目录下,然后运行`python generate4Txt.py`

8. 最后将VOCdevkit2007文件放到data文件夹下.

### 测试集:

1. af2019-cv-testA-20190318文件夹放置在preprocess文件夹下,运行`python merge3to1_train.py`

即可得到`merged_test`文件夹.

2. 将merged_test文件夹下生成的图片复制到StarFRCNN/images文件夹以供测试.

## 训练过程：

由于我们采用res101作为基础网络,在获取了与训练模型并且配置好数据集后,运行以下命令

```
CUDA_VISIBLE_DEVICES=$GPU_ID python trainval_net.py \
                   --dataset pascal_voc --net res101 \
                   --bs $BATCH_SIZE --nw $WORKER_NUMBER \
                   --lr $LEARNING_RATE --lr_decay_step $DECAY_STEP \
                   --cuda
```

举个例子:

```
CUDA_VISIBLE_DEVICES=0 python trainval_net.py \
                   --dataset pascal_voc --net res101 \
                   --bs 2 --nw 4 \
                   --lr 0.001 \
                   --cuda
```

## 测试过程：

### demo

将测试数据放到images目录以后,运行以下命令:

```
python demo.py --net res101 \
               --checksession $SESSION --checkepoch $EPOCH --checkpoint $CHECKPOINT \
               --cuda --load_dir path/to/model/directoy \
               --output_dir path/to/output/dir
```

举个例子:

```
python demo.py --net res101 \
               --checksession 1 --checkepoch 1 --checkpoint 2514 \
               --cuda --load_dir ./models \
               --output_dir ./output_image
```

注意:此时models的结构如下:

```
models
	- res101
		- pascal_voc
			- faster_rcnn_1_1_2514.pth(我们训练得到的权重)
```

最终得到的结果是图片上有框,对应confidence

### 如何得到submit.csv

```
python test_net.py --dataset pascal_voc --net res101 \
                   --checksession $SESSION --checkepoch $EPOCH \
                   --checkpoint $CHECKPOINT \
                   --cuda
```

举个例子:

```
python test_net.py --dataset pascal_voc --net res101 \
				    --checksession 1 --checkepoch 1 \
				    --checkpoint 2514 \
                    --cuda
```

使用的是faster_rcnn_1_1_2514.pth权重

然后运行命令:

```
cd data/VOCdevkit2007/results/VOC2007/Main
```

将preprocess.py文件中的`txt2csv_havestar.py`和`txt2csv_nostar.py`两个文件放到该目录下

此时该目录下会出现两个文件

> - comp4_det_test_havestar.txt
> - comp4_det_test_nostar.txt

此时先运行:`python txt2csv_havestar.py`然后运行`python txt2csv_nostar.py`,注意调用顺序,最终得到submit.csv

## 致谢

感谢队友们的支持，以及西北农林科技大学的宁教授思路上的支持，感谢主办方提供的比赛机会。