if __name__ == '__main__':
    f = open('result/merge_list.txt', 'w')
    for seg in range(30):
        f.write('file \'seg' + str(seg) + '_result.mp4\'\n')
    f.close()