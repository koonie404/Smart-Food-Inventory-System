import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque
import csv
from datetime import datetime

MODEL_PATH = 'best.pt'
VIDEO_PATH = r'C:\우재남_객체지향\Mini Project\Smart Buffet Food Monitor\뷔페\KakaoTalk_20260306_145612286.mp4'
CONF_TH = 0.50
LOG_PATH = r'C:\우재남_객체지향\Mini Project\Smart Buffet Food Monitor\뷔페\food_log.csv'
LOG_INTERVAL = 30  # 몇 프레임마다 CSV에 기록할지 (30 = 약 1초마다)

def calc_food_ratio(roi_bgr):
    h_img, w_img = roi_bgr.shape[:2]
    hsv = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)

    # 접시(흰색~밝은회색): S<40 인 영역
    plate_mask = cv2.inRange(hsv, np.array([0,0,130]), np.array([180,40,255]))
    kernel = np.ones((7,7), np.uint8)
    plate_mask = cv2.morphologyEx(plate_mask, cv2.MORPH_CLOSE, kernel)
    plate_mask = cv2.morphologyEx(plate_mask, cv2.MORPH_OPEN, kernel)
    plate_pixels = cv2.countNonZero(plate_mask)

    # 음식: S>=40 인 영역 (접시 제외)
    food_mask = cv2.inRange(hsv, np.array([0,40,30]), np.array([180,255,255]))
    food_mask = cv2.bitwise_and(food_mask, cv2.bitwise_not(plate_mask))

    # 노이즈 제거
    food_mask = cv2.morphologyEx(food_mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    food_mask = cv2.morphologyEx(food_mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))

    food_pixels = cv2.countNonZero(food_mask)

    # 접시 면적 기준으로 비율 계산
    base_area = max(plate_pixels, int(h_img * w_img * 0.3))
    ratio = (food_pixels / base_area) * 100.0
    ratio = min(ratio, 100.0)

    # debug = np.hstack([food_mask, plate_mask])
    # cv2.imshow('Debug (food | plate)', debug)

    return float(ratio)

def init_csv(path):
    import os
    if not os.path.exists(path):  # 파일이 없을 때만
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:  # 새로 만들고 헤더 작성
            writer = csv.writer(f)
            writer.writerow(['시간', '접시번호', '잔량(%)', '상태'])
    # 파일이 이미 있으면 아무것도 안 함 → log_csv가 'a'로 이어쓰기

def log_csv(path, plate_num, ratio, status_msg):
    with open(path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            f'접시{plate_num}',
            f'{ratio:.0f}',
            status_msg
        ])

def main():
    model = YOLO(MODEL_PATH)
    ratio_history = {}  # 박스별 히스토리
    frame_count = 0

    # CSV 초기화
    init_csv(LOG_PATH)
    print(f"[CSV] {LOG_PATH} 기록 시작")

    cap = cv2.VideoCapture(VIDEO_PATH)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        h, w = frame.shape[:2]
        annotated = frame.copy()

        results = model(frame, verbose=False, conf=CONF_TH, iou=0.3)

        plate_num = 0
        for result in results:
            if result.boxes is None:
                continue
            for i, box in enumerate(result.boxes.xyxy.cpu().numpy()):
                x1, y1, x2, y2 = map(int, box)

                # 작은 박스 제거
                if (x2-x1) < (w*0.25) or (y2-y1) < (h*0.25):
                    continue

                roi = frame[y1:y2, x1:x2]
                if roi.size == 0:
                    continue

                plate_num += 1

                # 잔량 계산
                ratio = calc_food_ratio(roi)

                # 스무딩 (5프레임 평균)
                box_key = f"{x1}_{y1}"
                if box_key not in ratio_history:
                    ratio_history[box_key] = deque(maxlen=5)
                ratio_history[box_key].append(ratio)
                ratio = float(np.mean(ratio_history[box_key]))  # 평균값 사용

                # 상태 판단
                if ratio <= 30:
                    status_msg, color = "FILL NOW", (0,0,255)
                elif ratio <= 65:
                    status_msg, color = "PREPARE", (0,165,255)
                else:
                    status_msg, color = "ENOUGH", (0,255,0)

                # CSV 기록 (LOG_INTERVAL 프레임마다)
                if frame_count % LOG_INTERVAL == 0:
                    log_csv(LOG_PATH, plate_num, ratio, status_msg)

                # 화면 표시
                text = f'{status_msg}: {ratio:.0f}%'
                font = cv2.FONT_HERSHEY_SIMPLEX
                (tw, th), _ = cv2.getTextSize(text, font, 0.6, 2)
                text_y = max(y1 - 10, th + 10)

                cv2.rectangle(annotated, (x1,y1), (x2,y2), color, 2)
                cv2.rectangle(annotated, (x1, text_y-th-6), (x1+tw+4, text_y+6), color, -1)
                cv2.putText(annotated, text, (x1+2, text_y), font, 0.6, (0,0,0), 2)

        # 우측 하단에 현재 시각 표시
        time_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(annotated, time_text, (w - 300, h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow('Smart Food Monitor', annotated)
        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"[완료] CSV 저장 위치: {LOG_PATH}")

if __name__ == '__main__':
    main()