import os

def calculate_weight(tile_x, tile_y, viewpoint_x, viewpoint_y):
    tile_left = tile_x * 320
    tile_right = tile_left + 320
    tile_up = tile_y * 240
    tile_down = tile_up + 240
    view_left = viewpoint_x - 640
    view_right = viewpoint_x + 640
    view_up = viewpoint_y - 360
    view_down = viewpoint_y + 360
    
    x1 = max(tile_left, view_left)
    y1 = max(tile_up, view_up)
    x2 = min(tile_right, view_right)
    y2 = min(tile_down, view_down)
    # print(str(x2-x1) + ' ' + str(y2-y1))
    return ((x2-x1) * (y2-y1)) / 320 / 240


def calculate_weighted_file_size(seg, tile_x, tile_y, weight):
    size = 0
    file_name_base = 'download\\seg' + str(seg) + '_tile' + str(tile_x) + '_' + str(tile_y) + '_L'
    if os.path.exists(file_name_base + '1.svc'):
        size = size + os.path.getsize(file_name_base + '1.svc')
        if os.path.exists(file_name_base + '2.svc'):
            size = size + os.path.getsize(file_name_base + '2.svc')
            if os.path.exists(file_name_base + '3.svc'):
                size = size + os.path.getsize(file_name_base + '3.svc')
    return weight * size


if __name__ == '__main__':
    viewpoint_file = open('viewpoint.txt', 'r')
    viewpoint_list = viewpoint_file.readlines()
    viewpoint_file.close()

    quality_sum = 0
    for seg in range(30):
        viewpoint_x = int(viewpoint_list[seg].split(' ')[0])
        viewpoint_y = int(viewpoint_list[seg].split(' ')[1])
        result_file = open('download/seg' + str(seg) +'_result.txt', 'r')
        tile_list = result_file.readlines()
        result_file.close()

        seg_total_quality = 0
        for tile in tile_list:
            tile_x = int(tile.split(' ')[0])
            tile_y = int(tile.split(' ')[1])
            tile_weight = calculate_weight(tile_x, tile_y, viewpoint_x, viewpoint_y)
            tile_quality = calculate_weighted_file_size(seg, tile_x, tile_y, tile_weight)
            # print('x:' + str(tile_x) + ' y:' + str(tile_y) + ' w:' + str(tile_weight) + ' q:' + str(tile_quality))
            seg_total_quality = seg_total_quality + tile_quality
        print('seg' + str(seg) + ' quality: ' + str(int(seg_total_quality)))
        quality_sum = quality_sum + seg_total_quality
    print(str(int(quality_sum)) + ' B in total')
