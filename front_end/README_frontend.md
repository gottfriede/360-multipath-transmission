# 客户端



## 文件结构

​	 `download/` : 用于存放从服务端获取的需要传输的视频块列表 `segT_result.txt` 以及从服务端下载的原始 `segT_tileX_Y_LN.svc` 文件。此外，还存放解码完成后的结果 `segT_tileX_Y.yuv` 。

​	 `result/` : 用于存放拼接以及裁剪的一些中间结果，分别有 `segT_tilexM.yuv` , `segT_all_tile.yuv` , `segT_result.yuv` ，最终可查看的结果为 `segT_result.mp4` 。

​	 `front_end_thread.py` : 客户端的请求与解码等流程均实现于此，同时统计卡顿频率。

​	 `calculate_quality.py` : 根据 `download/` 中的 `.svc` 文件计算有效流量。

​	 `gen_merge_file.py` : 用于生成 `result/merge_list.txt` ，该 `.txt` 在 `front_end_thread.py` 的将各个时间段的视频拼接时需要用到，因此在运行客户端前首先应运行一次 `gen_merge_file.py` 。

​	 `svc_merge.py` : 该文件由 `DASH-SVC-Toolchain` 提供，在解码过程中需要用到。

​	 `delete_tmp.py` : 将 `download/` 和 `result/` 都清空。

​	 `test.py` : 三条命令，测实验结果时可以使用。

​	 `viewpoint.txt` : 由 `front_end_thread.py` 生成，记录用户视点轨迹。

​	 `result.mp4` : 客户端最终结果。



