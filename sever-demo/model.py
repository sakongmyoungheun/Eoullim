import cv2
import mediapipe as mp
import json
import numpy as np
import torch
import torch.nn as nn
import os
from torchvision import datasets, models, transforms
import pandas as pd

data_df = pd.read_excel("./meaning.xlsx")

class ResNetCustom(nn.Module):
    def __init__(self, num_classes=3000):
        super(ResNetCustom, self).__init__()
        self.resnet = models.resnet50(pretrained=True)
        self.resnet.fc = nn.Linear(2048, num_classes)

    def forward(self, x):
        x = self.resnet.conv1(x)
        x = self.resnet.bn1(x)
        x = self.resnet.relu(x)
        x = self.resnet.maxpool(x)

        x = self.resnet.layer1(x)
        x = self.resnet.layer2(x)
        x = self.resnet.layer3(x)
        x = self.resnet.layer4(x)

        x = self.resnet.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.resnet.fc(x)

        return x
    
model = ResNetCustom().to('cpu')
checkpoint = torch.load('./model_test.pth', map_location=torch.device('cpu'))
model.load_state_dict(checkpoint)
model.eval()

# keypoint 뽑아오기
def video_landmark_dic(path):
    mp_hands = mp.solutions.hands

    img_list = []
    X_max, X_min, Y_max, Y_min = float('-inf'), float('inf'), float('-inf'), float('inf')
    i = 0
    # 영상 파일 열기
    cap = cv2.VideoCapture(path)

    # Mediapipe Hands 모델 초기화
    landmark_dic = {}
    landmark_x = []
    landmark_y = []
    start_frame_number = 0

    with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        # 영상에서 첫 번째 프레임만 읽기
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break
            # Mediapipe에 이미지 전달
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)

            # 손이 감지된 경우
            if results.multi_hand_world_landmarks:
                # start_frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
                for hand_landmarks, handedness in zip(results.multi_hand_world_landmarks, results.multi_handedness):
                    # 손의 라벨과 스코어 출력
                    hand_label = handedness.classification[0].label
                    hand_score = handedness.classification[0].score
                    # 각 랜드마크의 x, y 좌표와 손의 정확도, 프레임 번호, 키포인트 번호를 딕셔너리에 저장
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        landmark_x.append(landmark.x)
                        landmark_y.append(landmark.y)
                        landmark_dic[len(landmark_dic) + 1] = {'X': landmark.x, 'Y': landmark.y, 'C': hand_score, 't': int(frame_number) - int(start_frame_number), 'n': idx}
            else:
              start_frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
              if landmark_dic != {}:
                X_max, X_min, Y_max, Y_min = max(landmark_x), min(landmark_x), max(landmark_y), min(landmark_y)
                norm_dic = dic_normalization(landmark_dic, X_max, X_min, Y_max, Y_min)
                mapping_dic = mapping_fn(norm_dic)
                img = save_image_from_dict(mapping_dic)
                img_list.append(img)
                i += 1
                X_max, X_min, Y_max, Y_min = float('-inf'), float('inf'), float('-inf'), float('inf')
                landmark_dic = {}
                landmark_x = []
                landmark_y = []

        if landmark_dic != {}:
                start_frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
                X_max, X_min, Y_max, Y_min = max(landmark_x), min(landmark_x), max(landmark_y), min(landmark_y)
                norm_dic = dic_normalization(landmark_dic, X_max, X_min, Y_max, Y_min)
                mapping_dic = mapping_fn(norm_dic)
                img = save_image_from_dict(mapping_dic)
                img_list.append(img)
                i += 1
                X_max, X_min, Y_max, Y_min = float('-inf'), float('inf'), float('-inf'), float('inf')
                landmark_dic = {}
                landmark_x = []
                landmark_y = []

    ilist = run_model(img_list)
    cap.release()
    return ilist

def dic_normalization(dic, X_max, X_min, Y_max, Y_min):
    for idx, (k, v) in enumerate(dic.items()):
        X = (dic[k]['X'] - X_min) / (X_max - X_min)
        Y = (dic[k]['Y'] - Y_min) / (Y_max - Y_min)
        dic[k]['X'] = X
        dic[k]['Y'] = Y
    return dic

def mapping_fn(norm_dic):
    for i, (k, v) in enumerate(norm_dic.items()):
        R = norm_dic[k]['X'] * 255
        G = norm_dic[k]['Y'] * 255
        B = norm_dic[k]['C'] * 255

        norm_dic[k]['X'] = R
        norm_dic[k]['Y'] = G
        norm_dic[k]['C'] = B
    return norm_dic

def save_image_from_dict(data):
    # 이미지 크기 설정
    image_width = 224
    image_height = 224

    # 이미지 생성 (흰색 배경)
    image = np.full((image_height, image_width, 3), 0, dtype=np.uint8)

    # 데이터를 이미지에 플로팅
    for key, value in data.items():
        # C 값을 BGR 색상으로 변환
        color_r = value['X']  # X 값을 R로 사용
        color_g = value['Y']  # Y 값을 G로 사용
        color_b = value['C']
        x = value['n']  # n 값을 x좌표로 사용
        y = value['t']  # t 값을 y좌표로 사용

        # 이미지에 점 그리기
        cv2.circle(image, (x, y), radius=2, color=(color_b, color_g, color_r), thickness=-1)

    # 이미지 저장
    return image

def run_model(img_list):
    word_list = ''
    for img in img_list:
        img_tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).float()
        y_pred = model(img_tensor)
        y_pred_index = torch.argmax(y_pred).item()
        word = data_df.loc[data_df['index'] == y_pred_index, 'meaning'].values[0]
        word_list += word + ' '
    print(word_list) 
    return word_list