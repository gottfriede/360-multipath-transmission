import os

# split video by seconds (0:00 - 0:30)
def split_by_seconds():
    for i in range(30):
        start = '0:' + str(i)
        file_name = 'video/seg' + str(i) + '.mp4'
        # print('ffmpeg -ss %s -i original_video.mp4 -t 1 -c:v libx264 -c:a aac -strict experimental -b:a 96k %s' % (start, file_name))
        os.system('ffmpeg -ss %s -i video/original_video.mp4 -t 1 -c:v libx264 -c:a aac -strict experimental -b:a 96k %s' % (start, file_name))


# divide each seg(3840*1920) to 12*8 tiles
def divide_into_tile():
    for seg in range(30):
        input_file_name = 'video/seg' + str(seg) + '.mp4'
        for tile_x in range(12):
            for tile_y in range(8):
                start_x = tile_x * 320
                start_y = tile_y * 240
                output_file_name = 'video/seg' + str(seg) + '_tile' + str(tile_x) + '_' + str(tile_y) + '.mp4'
                # print('ffmpeg -i %s -vf crop=320:240:%s:%s %s -y' % (input_file_name, start_x, start_y, output_file_name))
                os.system('ffmpeg -i %s -vf crop=320:240:%s:%s %s -y' % (input_file_name, start_x, start_y, output_file_name))


# convert .mp4 to .yuv
def mp4_to_yuv():
    for seg in range(30):
        for tile_x in range(12):
            for tile_y in range(8):
                input_file_name = 'video/seg' + str(seg) + '_tile' + str(tile_x) + '_' + str(tile_y) + '.mp4'
                output_file_name = 'video/seg' + str(seg) + '_tile' + str(tile_x) + '_' + str(tile_y) + '.yuv'
                # print('ffmpeg -i %s %s' % (input_file_name, output_file_name))
                os.system('ffmpeg -i %s %s' % (input_file_name, output_file_name))


if __name__ == '__main__':
    split_by_seconds()
    divide_into_tile()
    mp4_to_yuv()