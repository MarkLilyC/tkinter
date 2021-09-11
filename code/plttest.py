import cv2
import fds_run
import fds_write

nums_list = []
back = None
for i in range(10):
    if i == 0:
        tmp, back = fds_write.cal((i+1) * 5, None)
        print(tmp)
        nums_list.append(tmp)
    else:
        tmp, back = fds_write.cal(i * 5, back)
        print(tmp)
        nums_list.append(tmp)
print(nums_list)
