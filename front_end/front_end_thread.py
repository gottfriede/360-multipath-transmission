import _thread as thread
import time
import requests
import json
import os
import eventlet

eventlet.monkey_patch()

server_tile_list_url = 'http://192.168.246.1:8080/api/tile_list/'
server1_download_url = 'http://192.168.246.1:8080/api/download/'
server2_download_url = 'http://192.168.242.200:8080/api/download/'

mode = 1 # 1 means transmit part of tiles, 2 means transmit all tiles
generate_final_result = True # True means generate the final result video, False means just check stall without decoding

viewpoint_list = []
time_list = []

'''
    Use the Python decorator to limit the run_time of the function
    It is based on eventlet package, I stole it from Internet
'''
def is_timeout(time_num):
    def wrap(func):
        def inner(*args, **kwargs):
            try:
                with eventlet.Timeout(time_num, True):
                    func(*args, **kwargs)
                return True
            except eventlet.timeout.Timeout:
                return False
        return inner
    return wrap


'''
    Function: Generate a list of user's viewpoint, save as viewpoint.txt
    Modify this function to generate more specific viewpoint movements
'''
def gen_viewpoint():
    f = open('viewpoint.txt', 'w')
    x = 1300
    y = 720
    for i in range(15):
        f.write(str(x) + ' ' + str(y) + '\n')
        x = (x + 70) % 3840
    for i in range(5):
        f.write(str(x) + ' ' + str(y) + '\n')
        y = (y + 30) % 1920
    for i in range(10):
        f.write(str(x) + ' ' + str(y) + '\n')
        x = (x - 50) % 3840
        y = (y - 10) % 1920
    f.close()


'''
    Function: Request the list of tiles needed to transmit based on the current user viewpoint, save as download/segT_result.txt
    Input: seg(int), Current time
'''
def request_tile_list(seg):
    viewpoint_x = viewpoint_list[seg].split(' ')[0]
    viewpoint_y = viewpoint_list[seg].split(' ')[1]
    # print('Request: seg' + str(seg) + ' viewpoint: ' + viewpoint_x + ' ' + viewpoint_y)

    header = {'Content-Type': 'application/json;charset=UTF-8'}
    body = {
        'seg': seg,
        'viewpoint_x': viewpoint_x,
        'viewpoint_y': viewpoint_y
    }
    respose = requests.post(url=server_tile_list_url, headers=header, data=json.dumps(body))
    # print(json.loads(respose.content))
    result_list = json.loads(respose.content)['res']

    res_file_name = 'download/seg' + str(seg) + '_result.txt'
    res_f = open(res_file_name, 'w')
    for tile in result_list:
        res_f.write(str(tile[0]) + ' ' + str(tile[1]) + '\n')
    res_f.close()    


'''
    Function: Generate a download/segT_result.txt which contains all tiles
    NOTICE: This function is used ONLY in the policy of transmitting all tiles, mode = 2
'''
def gen_all_tile(seg):
    file_name = 'download/seg' + str(seg) + '_result.txt'
    file = open(file_name, 'w')
    for x in range(12):
        for y in range(8):
            file.write(str(x) + ' ' + str(y) + '\n')
    file.close()


'''
    Function: Request a single layer file from the server at the specified IP address, save as download/segT_tileX_Y_LN.svc
    Input: seg(int), tile_x(int), tile_y(int), layer(int, from 1 to 3), Some parameters used to locate the file
    Input: server(int, 1 or 2), Corresponds to different IP addresses
'''
def request_download(seg, x, y, layer, server):
    header = {'Content-Type': 'application/json;charset=UTF-8'}
    body = {
        'seg': seg,
        'x': x,
        'y': y,
        'layer': layer
    }
    if server == 1:
        respose = requests.post(url=server1_download_url, headers=header, data=json.dumps(body))
    if server == 2:
        respose = requests.post(url=server2_download_url, headers=header, data=json.dumps(body))
    file_name = 'download\\seg' + str(seg) + '_tile' + str(x) + '_' + str(y) + '_L' + str(layer) + '.svc'
    f = open(file_name, 'wb')
    f.write(respose.content)
    f.close()


'''
    Function: Use DASH-SVC-Toolchain and JSVM decoder to merge and decode a tile, save as download/segT_tileX_Y.yuv
    Input: seg(int), tile_x(int), tile_y(int), Some parameters used to locate a tile
    NOTICE: I can ONLY successfully decode ONE base layer and ONE enhancement layer, so the command is written directly here
            Please refer to DASH-SVC-Toolchain and JSVM for more usages of the decoder
'''
def decode(seg, x, y):
    command = 'python2 svc_merge.py download\\seg' + str(seg) + '_tile' + str(x) + '_' + str(y) + '.264 download\\seg'  + str(seg) + '_tile' + str(x) + '_' + str(y) + '_L1.svc download\\seg'  + str(seg) + '_tile' + str(x) + '_' + str(y) + '_L2.svc'
    os.system(command)
    command = 'H264AVCDecoderLibTestStaticd download\\seg' + str(seg) + '_tile' + str(x) + '_' + str(y) + '.264 download\\seg'  + str(seg) + '_tile' + str(x) + '_' + str(y) + '.yuv'
    os.system(command)

'''
    Function: Copy .yuv files directly from local instead of network transmission and encode process
    NOTICE: It is a TRICK, ONLY used when the 5G station is not turned on, to check the correctness of the rest of client process
'''
def move(seg):
    res_file_name = 'download\\seg' + str(seg) + '_result.txt'
    f = open(res_file_name, 'r')
    line_list = f.readlines()
    for line in line_list:
        tile_x = line.split(' ')[0]
        tile_y = line.split(' ')[1].split('\n')[0]
        yuv_file_name = '..\\video\\seg' + str(seg) + '_tile' + tile_x + '_' + tile_y + '.yuv'
        # print('copy ' + yuv_file_name + ' res\\')
        os.system('copy ' + yuv_file_name + ' download\\')
    f.close()

'''
    Function: Merge tiles of the same segment, save as segT_all_tile.yuv
    Input: seg(int), Time
    Output: x_num(int), y_num(int), Indicates how many tiles this segment is made up of in the vertical and horizontal
'''
def tile_merge(seg):
    yuv_list = []
    res_file_name = 'download/seg' + str(seg) + '_result.txt'
    f = open(res_file_name, 'r')
    line_list = f.readlines()
    yuv_x_list = []
    last_tile_x = -1
    for line in line_list:
        tile_x = line.split(' ')[0]
        tile_y = line.split(' ')[1].split('\n')[0]
        yuv_file_name = 'download\\seg' + str(seg) + '_tile' + tile_x + '_' + tile_y + '.yuv'
        if not tile_x == last_tile_x:
            yuv_list.append(yuv_x_list)
            yuv_x_list = []
        yuv_x_list.append(yuv_file_name)
        last_tile_x = tile_x
    yuv_list.append(yuv_x_list)
    f.close()
    # print(yuv_list)

    x_num = len(yuv_list) - 1
    y_num = 0
    now_x_num = 0
    for yuv_x_list in yuv_list:
        if yuv_x_list:
            # print(yuv_x_list)
            now_x_num = now_x_num + 1
            y_num = len(yuv_x_list)
            command = 'ffmpeg -f rawvideo'
            for yuv_file in yuv_x_list:
                command = command + ' -video_size 320x240 -i ' + yuv_file
            command = command + ' -filter_complex \"[0:v]pad=iw:ih*' + str(y_num) + '[a]' 
            for i in range(y_num-1):
                command = command + ';[' + chr(i+ord('a')) + '][' + str(i+1) + ':v]overlay=0:h*' + str(i+1) + '[' + chr(i+1+ord('a')) + ']'
            command = command[:-3]
            command = command + '\" result\\seg' + str(seg) + '_tilex' + str(now_x_num) + '.yuv'
            print(command)
            os.system(command)
            print()

    resolution = '320x' + str(y_num*240)
    command = command = 'ffmpeg -f rawvideo'
    for i in range(x_num):
        command = command + ' -video_size ' + resolution + ' -i result\\seg' + str(seg) + '_tilex' + str(i+1) +'.yuv'
    command = command + ' -filter_complex \"[0:v]pad=iw*' + str(x_num) +':ih[a]' 
    for i in range(x_num-1):
        command = command + ';[' + chr(i+ord('a')) + '][' + str(i+1) + ':v]overlay=w*' + str(i+1) + ':0[' + chr(i+1+ord('a')) + ']'
    command = command[:-3]
    command = command + '\" result\\seg' + str(seg) + '_all_tile.yuv'
    # print(command + '\n')
    os.system(command)
    return [x_num, y_num]


'''
    Function: Crop the result video according to the user's viewpoint, save as segT_result.yuv(1280x720)
    Input: seg(int), Time
    Input: x_num(int), y_num(int), Indicates how many tiles this segment is made up of in the vertical and horizontal, computed by function tile_merge
'''
def crop(seg, x_num, y_num):
    point_x = int(viewpoint_list[seg].split(' ')[0])
    point_y = int(viewpoint_list[seg].split(' ')[1])
    true_left = point_x - 640
    true_up = point_y - 360
    result_f = open('download/seg' + str(seg) +'_result.txt', 'r')
    first_line = result_f.readline()
    tile_x = int(first_line.split(' ')[0])
    tile_y = int(first_line.split(' ')[1].split('\n')[0])
    tile_left = tile_x * 320
    tile_up = tile_y * 240
    result_f.close()
    # print(str(true_left) + ' ' + str(true_up) + ' ' + str(tile_left) + ' ' + str(tile_up))
    delta_x = true_left - tile_left
    delta_y = true_up - tile_up
    resolution = str(x_num*320) + 'x' + str(y_num*240)
    command = 'ffmpeg -s ' + resolution + ' -i result\\seg' + str(seg) + '_all_tile.yuv -vf crop=1280:720:' + str(delta_x) + ':' + str(delta_y) + ' result\\seg' + str(seg) + '_result.yuv'
    print(command+ '\n')
    os.system(command)


'''
    Function: Use ffplay to play .yuv intermediate results
'''
def play_video(seg):
    command = 'ffplay -autoexit -video_size 1280x720 -i result\\seg' + str(seg) + '_result.yuv'
    os.system(command)


'''
    Function: Merge the videos of each segment, save as result.mp4, this is the final result
'''
def time_merge():
    for seg in range(30):
        command = 'ffmpeg -s 1280x720 -i result\\seg' + str(seg) + '_result.yuv result\\seg' + str(seg) + '_result.mp4'
        os.system(command)
    command = 'ffmpeg -f concat -safe 0 -y -i result\\merge_list.txt -c copy -strict -2 result.mp4'
    os.system(command)


'''
    Function: Delete intermediate results in /download and /result
'''
def delete_tmp():
    for file_name in os.listdir('result\\'):
        if not file_name.endswith('merge_list.txt'):
            os.remove('result\\' + file_name)
    
    for file_name in os.listdir('download\\'):
        os.remove('download\\' + file_name)


'''
    Function: A time-limited thread function which requests a specific layer from a specific server IP address
    Input: seg(int), Time
    Input: tile_list(list), layer_list(list)
    Input: server(int, 1 or 2)
'''
@is_timeout(1)
def thread_download_tile(seg, tile_list, layer_list, server):
    for layer in layer_list:
        for line in tile_list:
            x = line.split(' ')[0]
            y = line.split(' ')[1].split('\n')[0]
            request_download(seg, x, y, layer, server)


'''
    Function: Start the sub-thread for downloading
'''
def download_in_time_limit(seg):
    if mode == 1:
        request_tile_list(seg)
    if mode == 2:
        gen_all_tile(seg)
    tile_list_file = open('download\\seg' + str(seg) + '_result.txt')
    tile_list = tile_list_file.readlines()
    thread.start_new_thread(thread_download_tile, (seg, tile_list, [1], 1))
    thread.start_new_thread(thread_download_tile, (seg, tile_list, [2,3], 2))


'''
    Function: Determine whether there is a stall according to the base layer files in /download
    Input: seg(int), Time
    Output: res(bool)
'''
def check_stall(seg):
    res = False

    tile_list_file = open('download\\seg' + str(seg) + '_result.txt')
    tile_list = tile_list_file.readlines()
    for line in tile_list:
        x = line.split(' ')[0]
        y = line.split(' ')[1].split('\n')[0]
        base_layer_file_name = 'download\\seg' + str(seg) + '_tile' + str(x) + '_' + str(y) + '_L1.svc'
        if not os.path.exists(base_layer_file_name):
            # print('Lack of ' + base_layer_file_name)
            res = True
            return res
    return res


if __name__ == '__main__':
    gen_viewpoint()     # Generate user's viewpoint
    viewpoint_file = open('viewpoint.txt', 'r')
    viewpoint_list = viewpoint_file.readlines()
    viewpoint_file.close()

    if generate_final_result:       # This process is used to generate the final result video
        for seg in range(30):
            request_tile_list(seg)
            tile_list_file = open('download\\seg' + str(seg) + '_result.txt')
            tile_list = tile_list_file.readlines()

            for line in tile_list:
                x = line.split(' ')[0]
                y = line.split(' ')[1].split('\n')[0]
                request_download(seg, x, y, 1, server=1)
                request_download(seg, x, y, 2, server=2)
                request_download(seg, x, y, 3, server=2)
                decode(seg, x, y)
            # move(seg)             # If test locally, use move() instead of request_download()
            
            [x_num, y_num] = tile_merge(seg)
            crop(seg, x_num, y_num)
        time_merge()

    else:                           # This process is used to test the stall frequency without decoding and so on
        stall_num = 0
        for seg in range(30):
            download_in_time_limit(seg)     # request and download
            time.sleep(1)
            if check_stall(seg):        # The main thread pauses for 1s and then check whether stall happens
                stall_num = stall_num + 1
                print('Stall at seg ' + str(seg))
        print('Stall times: ' + str(stall_num))
    
    delete_tmp()
