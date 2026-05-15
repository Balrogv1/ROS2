import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 获取功能包share目录的绝对路径

def main():
    default_image_path = get_package_share_directory('demo_python_service') + '/resource/bus.jpg'
    print(f'图片的真实路劲：{default_image_path}')
    image = cv2.imread(default_image_path)
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=2, model='hog')
    print(f'识别到的人脸个数：{len(face_locations)}')
    for face_location in face_locations:
        top, right, bottom, left = face_location
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()