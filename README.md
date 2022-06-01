# Generate Static Resources

Follow these steps to generate static resources(`*.svc`).



## Download Video

Download a 360 degree video from YouTube, example [here](https://www.youtube.com/watch?v=uZGrikvGen4) .



## Video Preprocess

Call `video_preprocess.py` to use `ffmpeg` to preprocess video downloaded.

`ffmpeg` example usage: 

```
// change EAC to E
ffmpeg -i input.mp4 -vf v360=eac:e output.mp4

// cut to 60 seconds
ffmpeg -ss 0:00 -i input.mp4 -t 60 -c:v copy -c:a copy output.mp4

// change mp4 to yuv
ffmpeg -i input.mp4 output.yuv

// split video by seconds
ffmpeg -ss 0:00 -i input.mp4 -t 1 -c:v libx264 -c:a aac -strict experimental -b:a 96k output.mp4
```

More usage can be seen [here](https://blog.csdn.net/qiutiantxwd/article/details/107283224) and [here](https://blog.csdn.net/xuejianbest/article/details/84774136) .



## Download and build encoder/decoder

`SVC_toolchain` is a toolchain for _Scalable Video Coding_ (SVC). This toolkit provides scripts for encoding and decoding video or demultiplexing and re-multiplexing video content which has been encoded according to the **H.264/SVC** extension. It is from [DASH-SVC-Toolchain](https://github.com/ChristianKreuzberger/DASH-SVC-Toolchain) and can be used together with their [Dataset](http://concert.itec.aau.at/SVCDataset/) .

#### Dependencies

* Python 2.7
* Python pip
* Python module: bitstring
* CVS (required for downloading JSVM)
* build-essentials and cmake
* [JSVM](http://www.hhi.fraunhofer.de/de/kompetenzfelder/image-processing/research-groups/image-video-coding/svc-extension-of-h264avc/jsvm-reference-software.html) Reference Encoder
* [libdash](https://github.com/bitmovin/libdash) library for parsing MPD files

### Download and Build

Create a directory called SVC and switch to this directory then follow the steps below:

	# Requires: python (2.7), cvs, git
	# libdash requires:
	sudo apt-get install cvs git-core build-essential cmake libxml2-dev libcurl4-openssl-dev python-pip
	
	# python setup-tools (easy install)
	sudo apt-get install python-setuptools
	# python module bitstring
	sudo pip install bitstring
	
	# mplayer for playing yuv files
	sudo apt-get install mplayer
	
	# get this repository
	git clone --recursive git://github.com/ChristianKreuzberger/DASH-SVC-Toolchain.git
	cd DASH-SVC-Toolchain


Call the script `build_scripts/buildLibDash.sh` to **build libdash** :

	chmod 777 build_scripts/buildLibDash.sh
	build_scripts/buildLibDash.sh

Create a directory called jsvm and download code [here](https://github.com/floriandejonckheere/jsvm), then **build JSVM** via make:

	cd jsvm/JSVM/H264Extension/build/linux
	make
	
	# see if the JSVM tools exist
	cd ../../../../bin/
	ls
	
	# go back to the main directory
	cd ../../

Add JSVM to **PATH**:

```
vim /etc/profile
# append this
export PATH=”$PATH:home/multipath/SVC/jsvm/bin” 

# Test whether corrctly added to path
H264AVCDecoderLibTestStatic
```



## Encode

Call `encode_all.py` to use `JSVM` to encode all the `video/segA_tileX_Y.yuv` in SVC.

We encode each to 1 base layer (`static_svc/segA_tileX_Y_L1`) and 2 enhancement layer (`static_svc/segA_tileX_Y_L2` , `static_svc/segA_tileX_Y_L3`).