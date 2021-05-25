# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(S):

    size_by_type = [0] * 4
    filetype = {'mp3': 0, 'aac': 0, 'flac': 0, 'jpg': 1, 'bmp': 1, 'gif': 1, 'mp4':2, 'avi':2, 'mkv':2}

    # 파일 분리
    file_list = list(map(str,S.split('\n')))
    for file_info in file_list:
        # 이름, 사이즈 분리
        file_name, file_size = map(str,file_info.split())
        # 타입 분리
        file_type = list(map(str, file_name.split(".")))[-1]
        # 사이즈 숫자 분리
        byte_size = int(file_size[:-1])

        # 타입별 사이즈 계산
        if file_type in filetype:
            size_by_type[filetype[file_type]] += byte_size
        else:
            size_by_type[3] += byte_size

    # 정답 문자열
    return "music "+ str(size_by_type[0]) +"b\n" + "images "+ str(size_by_type[1]) +"b\n" + "movies "+ str(size_by_type[2]) +"b\n" + "other "+ str(size_by_type[3]) +"b\n"

