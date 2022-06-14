# 客户端



## 文件结构

​		 `download/` : 用于存放从服务端获取的需要传输的视频块列表 `segT_result.txt` 以及从服务端下载的原始 `segT_tileX_Y_LN.svc` 文件。此外，还存放解码完成后的结果 `segT_tileX_Y.yuv` 。

​		 `result/` : 用于存放拼接以及裁剪的一些中间结果，分别有 `segT_tilexM.yuv` , `segT_all_tile.yuv` , `segT_result.yuv` ，最终可查看的结果为 `segT_result.mp4` 。

​		 `front_end_thread.py` : 客户端的请求与解码等流程均实现于此，同时统计卡顿频率。

​		 `calculate_quality.py` : 根据 `download/` 中的 `.svc` 文件计算有效流量。

​		 `gen_merge_file.py` : 用于生成 `result/merge_list.txt` ，该 `.txt` 在 `front_end_thread.py` 的将各个时间段的视频拼接时需要用到，因此在运行客户端前首先应运行一次 `gen_merge_file.py` 。

​		 `svc_merge.py` : 该文件由 `DASH-SVC-Toolchain` 提供，在解码过程中需要用到。

​		 `delete_tmp.py` : 将 `download/` 和 `result/` 都清空。

​		 `test.py` : 三条命令，测实验结果时可以使用。

​		 `viewpoint.txt` : 由 `front_end_thread.py` 生成，记录用户视点轨迹。

​		 `result.mp4` : 客户端最终结果。



## 一些命令示例

​		解码：现在我只能成功解码一个基础层和一个增强层的情况，因此此命令可能存在问题，关于解码器的更多使用方法请参考 [DASH-SVC-Toolchain](https://github.com/ChristianKreuzberger/DASH-SVC-Toolchain) 。

```shell
python2 svc_merge.py tile.264 L1.svc L2.svc
H264AVCDecoderLibTestStaticd tile.264 tile.yuv
```

​		tile在空间纵向与横向上的合并（以4个为例）：更多可参考 [这里](https://blog.csdn.net/a386115360/article/details/89465633) 。

```shell
ffmpeg -f rawvideo -video_size 320x240 -i tile1.yuv -video_size 320x240 -i tile2.yuv -video_size 320x240 -i tile3.yuv -video_size 320x240 -i tile4.yuv -filter_complex "[0:v]pad=iw:ih*4[a];[a][1:v]overlay=0:h*1[b];[b][2:v]overlay=0:h*2[c];[c][3:v]overlay=0:h*3" result.yuv
ffmpeg -f rawvideo -video_size 320x240 -i tile1.yuv -video_size 320x240 -i tile2.yuv -video_size 320x240 -i tile3.yuv -video_size 320x240 -i tile4.yuv -filter_complex "[0:v]pad=iw*4:ih[a];[a][1:v]overlay=w*1:0[b];[b][2:v]overlay=w*2:0[c];[c][3:v]overlay=w*3:0" result.yuv
```

​		裁剪：

```shell
ffmpeg -s 1920*1200 -i all_tile.yuv -vf crop=1280:720:100:200 result.yuv
```

​		播放 `.yuv` 视频：

```shell
ffplay -video_size 1920x960 -i result.yuv
```

​		 `.yuv` 转换为 `.mp4` 视频：

```shell
ffmpeg -s 1280x720 -i result.yuv result.mp4
```

​		segment在时间上的拼接（需要 `merge_list.txt` ）：

```
ffmpeg -f concat -safe 0 -y -i merge_list.txt -c copy -strict -2 result.mp4
```

