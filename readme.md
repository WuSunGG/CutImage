# 应用场景
以原图( .bmp )中心点作为目标图片的中心点，将图片剪裁为分辨率为750*350的图片

# 环境要求
python 3.6+

# 安装依赖
> pip install pillow
>
# 用法
> python transmit.py 要转换的文件夹 [输出的文件夹]

默认输出文件为当前目标的 target 目录

例：
未指定 \[输出的文件夹\], 默认输出到 ./target . 以下例子输出到 D:\GZUniversity\CutImage\target 文件夹中
> python transmit.py D:\GZUniversity\CutImage\sfj 

例：
指定输出文件夹
> python transmit.py D:\GZUniversity\CutImage\sfj D:\GZUniversity\CutImage\target1
