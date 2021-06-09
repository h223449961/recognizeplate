import cv2
binary_threshold = 97
segmentation_spacing = 0.93
img = cv2.imread('02.jpeg')
img = cv2.resize(img,(1000,500))
'''
將照片灰化，並二值化
'''
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imshow('gray',img_gray)
cv2.waitKey(0)
img_thre = img_gray
cv2.threshold(img_gray, binary_threshold, 255, cv2.THRESH_BINARY_INV, img_thre)
cv2.imshow('threshold', img_thre)
cv2.waitKey(0)
'''
每一列的白像素總和
'''
white = []
'''
每一列的黑像素總和
'''
black = []
height = img_thre.shape[0]
width = img_thre.shape[1]
'''
只保存每列中白最多的像素總數
'''
white_max = 0
'''
只保存每列中黑最多的像素總數
'''
black_max = 0
'''
for loor 計算每一列的黑白像素總和
'''
for i in range(width):
    '''
    此列的白像素總數
    '''
    w_count = 0
    '''
    此列的黑像素總數
    '''
    b_count = 0
    for j in range(height):
        if img_thre[j][i] == 255:
            w_count += 1
        else:
            b_count += 1
    white_max = max(white_max, w_count)
    black_max = max(black_max, b_count)
    white.append(w_count)
    black.append(b_count)
'''
true 表示黑底白字
false 表示白底黑字
'''
arg = black_max > white_max
'''
分割照片
'''
def find_end(start_):
    end_ = start_ + 1
    for m in range(start_+1, width - 1):
        if(black[m] if arg else white[m]) > (segmentation_spacing * black_max if arg else segmentation_spacing * white_max):
            end_ = m
            break
    return end_
n = 1
start = 1
end = 2
while n < width - 1:
    n += 1
    '''
    判斷是白底黑字還是黑底白字
    '''
    if(white[n] if arg else black[n]) > ((1 - segmentation_spacing) * white_max if arg else (1 - segmentation_spacing) * black_max):
        start = n
        end = find_end(start)
        n = end
        if end - start > 5:
            print(start, end)
            cj = img_thre[1:height, start:end]
            cv2.imshow('cutChar', cj)
            cv2.waitKey(0)