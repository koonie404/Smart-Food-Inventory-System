🥗 Vision AI 기반 스마트 푸드 재고 관리 및 모니터링 시스템

Real-time Food Inventory Management & Monitoring System using YOLOv8 & HSV Analysis

0. 핵심 요약 (Executive Summary)

목표: 수동 확인 방식의 급식/뷔페 배식 관리 시스템을 Vision AI로 자동화하여 인건비 절감 및 운영 효율 증대.

핵심 기술: YOLOv8 (객체 탐지) + HSV Color Masking (잔량 분석) + Multi-Object Tracking (개별 접시 추적).

성과: 5프레임 이동 평균 필터를 통한 노이즈 제거로 정밀한 실시간 잔량 산출 및 데이터 로깅 구현.

1. 프로젝트 개요 (Project Overview)

기존의 인력 중심 수동 확인 방식은 대응 지연과 불필요한 인건비를 발생시킵니다. 본 프로젝트는 카메라 기반 실시간 자동 감지 및 리필 알림 서비스를 통해 식자재 낭비를 최소화하고 고객 만족도를 극대화하는 것을 목표로 합니다.

🎥 프로젝트 시연 (Demo Video)



https://github.com/user-attachments/assets/120e137c-fdd2-4e64-9aa0-03207572560f







<em>실시간 접시 탐지 및 잔량 분석 구동 화면</em>
</p>

2. 시스템 아키텍처 (System Architecture)

🛠 개발 환경 (Development Environment)

Language: Python

AI Models: YOLOv8 (Ultralytics)

Tools: Roboflow, Google Colab, OpenCV

Library: Numpy, Pandas, Matplotlib

📐 아키텍처 구조

<img width="623" height="536" alt="image" src="https://github.com/user-attachments/assets/8700ab7e-454f-4e0b-b7bc-28c95483cb70" />


Input: 카메라 또는 MP4 영상 소스 입력.

Detection: YOLOv8 모델이 접시(Plate) 위치를 실시간 검출.

Analysis: 검출된 영역(ROI) 내 HSV 색상 분석을 통한 음식 잔량 계산.

Output: 실시간 시각화(Enough / Prepare / Fill) 및 CSV 데이터 로깅.

3. 핵심 알고리즘 (Key Algorithms)

3.1 하이브리드 잔량 분석 (Hybrid Analysis)

단순한 객체 탐지를 넘어, 비지도 학습 기반의 영상 처리를 결합하여 정밀도를 높였습니다.

HSV Masking: 조명 변화에 강인한 HSV 색 공간을 활용하여 음식 영역 분리.

Adaptive Threshold: 접시별 독립적인 ROI 추출 및 픽셀 비율 계산.

3.2 신뢰성 최적화 (Reliability Optimization)

Smoothing Filter: 배식 중 집게나 손에 의한 일시적 가림 현상을 방지하기 위해 5프레임 이동 평균 필터를 적용하여 수치 안정화.

Multi-ID Tracking: 각 접시에 고유 ID를 부여하여 개별적인 리필 상태 추적.

4. 실행 결과 (Results)

분석 단계

이미지 가이드

설명

Step 1. Detection

<img width="926" height="742" alt="스크린샷 2026-03-11 195321" src="https://github.com/user-attachments/assets/954f26a8-539c-4a03-b86a-f7a4802a1d00" />


YOLOv8을 통한 다중 접시 탐지

Step 2. Masking
<img width="1343" height="485" alt="스크린샷 2026-03-11 170057" src="https://github.com/user-attachments/assets/b339da9a-4a8d-407f-82c1-e23cd61aeae8" />



음식 영역 픽셀 추출 (HSV)

Step 3. Result
<img width="1538" height="737" alt="스크린샷 2026-03-26 104411" src="https://github.com/user-attachments/assets/16bdbe81-59f1-4233-b341-8dd8938dfc30" />



실시간 상태 표시 (FILL/ENOUGH)

5. 프로젝트 회고 (Reflection)

기술적 통찰: 지도학습(YOLO)과 비지도학습(영상처리)의 결합을 통해 데이터 라벨링의 한계를 극복하고 범용적인 분석 로직을 구축함.

향후 계획: 누적된 로그 데이터를 활용하여 메뉴별 소비 패턴 분석 AI 모델로 확장 예정.

6. 설치 및 실행 (Setup & Usage)

# 저장소 복제
git clone [https://github.com/YourUsername/Smart-Food-Monitoring.git](https://github.com/YourUsername/Smart-Food-Monitoring.git)

# 가상환경 설정 및 패키지 설치
pip install -r requirements.txt

# 시스템 실행
python main.py --source video.mp4


© 2026 임청수. All rights reserved. (임베디드 & 지능로봇 개발 과정)
