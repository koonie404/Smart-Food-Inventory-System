🥗 Vision AI 기반 스마트 푸드 재고 관리 및 모니터링 시스템

Real-time Food Inventory Management & Monitoring System using YOLOv8 & HSV Analysis

0. 핵심 요약 (Executive Summary)

목표: 수동 확인 방식의 급식/뷔페 배식 관리 시스템을 Vision AI로 자동화하여 인건비 절감 및 운영 효율 증대.

핵심 기술: YOLOv8 (객체 탐지) + HSV Color Masking (잔량 분석) + Multi-Object Tracking (개별 접시 추적).

성과: 5프레임 이동 평균 필터를 통한 노이즈 제거로 정밀한 실시간 잔량 산출 및 데이터 로깅 구현.

1. 프로젝트 개요 (Project Overview)

기존의 인력 중심 수동 확인 방식은 대응 지연과 불필요한 인건비를 발생시킵니다. 본 프로젝트는 카메라 기반 실시간 자동 감지 및 리필 알림 서비스를 통해
식자재 낭비를 최소화하고 고객 만족도를 극대화하는 것을 목표로 합니다.

## 🛡️ 핵심 강점 (Key Strengths & Data Reliability)
- **높은 데이터 신뢰성:** 5-Frame Moving Average Filter를 적용하여 배식 중 집게나 손에 의한 일시적 가림(Occlusion) 현상에도 안정적인 수치 유지.
  
- **정밀한 잔량 분석:** 조명 변화에 강한 HSV 색 공간 마스킹을 활용하여 접시 내부의 음식 영역만 픽셀 단위로 정확히 산출.

- **실시간 데이터 자산화:** 분석된 모든 재고 상태를 CSV 로그로 자동 저장하여 향후 메뉴 선호도 분석 및 수요 예측 데이터로 활용 가능.

  
🎥 프로젝트 시연 (Demo Video)



https://github.com/user-attachments/assets/120e137c-fdd2-4e64-9aa0-03207572560f







<em>실시간 접시 탐지 및 잔량 분석 구동 화면</em>
</p>

2. 시스템 아키텍처 (System Architecture)

### 🛠 개발 환경 및 성능 (Environment & Performance)
- **Language:** Python
  
- **AI Models:** YOLOv8 Nano (경량화 모델로 실시간성 확보)

- **Model Performance:** **mAP50 기준 89.2% 달성** (학습 결과 기준)

- **Tools:** Roboflow, Google Colab, OpenCV

📐 아키텍처 구조

<img width="623" height="536" alt="image" src="https://github.com/user-attachments/assets/8700ab7e-454f-4e0b-b7bc-28c95483cb70" />


Input: 카메라 또는 MP4 영상 소스 입력.

Detection: YOLOv8 모델이 접시(Plate) 위치를 실시간 검출.

Analysis: 검출된 영역(ROI) 내 HSV 색상 분석을 통한 음식 잔량 계산.

Output: 실시간 시각화(Enough / Prepare / REFILL) 및 CSV 데이터 로깅.

3. 핵심 알고리즘 (Key Algorithms)

3.1 하이브리드 잔량 분석 (Hybrid Analysis)

단순한 객체 탐지를 넘어, 비지도 학습 기반의 영상 처리를 결합하여 정밀도를 높였습니다.

- **HSV Masking (강점):** 단순한 픽셀 카운팅이 아니라, 조명 변화에 강인한 **HSV 색 공간**을 활용하여 식판의 반사광 노이즈를 최소화하고 순수 음식 영역만 정밀하게 추출함.
  
- **Adaptive Threshold:** 접시별 독립적인 ROI 추출 및 픽셀 비율 계산.

3.2 신뢰성 최적화 (Reliability Optimization)

Smoothing Filter: 배식 중 집게나 사람의 손에 의해 접시가 일시적으로 가려지는 현상(Occlusion)을 방지하기 위해 
5프레임 이동 평균 필터를 적용하여 잔량 수치의 급격한 변화를 막고 안정화함.

Multi-ID Tracking: 각 접시에 고유 ID를 부여하여 개별적인 리필 상태를 추적함으로써 데이터가 뒤섞이지 않도록 신뢰성을 확보함.

4. 실행 결과 (Results)

## 4. 실행 결과 (Results)

| 분석 단계 | 이미지 가이드 | 설명 |
| :--- | :---: | :--- |
| **Step 1. Detection** | <a href="https://github.com/user-attachments/assets/c9dc5db6-8a98-4fa8-abb9-b4a322779b12">
  <img width="300" src="https://github.com/user-attachments/assets/c9dc5db6-8a98-4fa8-abb9-b4a322779b12" alt="Detection 결과">
</a> | YOLOv8을 통한 다중 접시 탐지 |
| **Step 2. Masking** | <img width="300" height="300" alt="스크린샷 2026-03-11 170057" src="https://github.com/user-attachments/assets/b60ceb98-190a-4dd7-b426-61e2223147fd" /> | 음식 영역 픽셀 추출 (HSV) |
| **Step 3. Result** | <img width="300" height="300" alt="스크린샷 2026-03-26 104411" src="https://github.com/user-attachments/assets/f3aaa148-06d3-433d-8052-ea3d3307cf8d" /> | 실시간 상태 표시 (Enough / Prepare / REFILL) |


실시간 상태 표시 (Enough / Prepare / REFILL)

5. 프로젝트 회고 (Reflection)

기술적 통찰: 지도학습(YOLO)과 비지도학습(영상처리)의 결합을 통해 데이터 라벨링의 한계를 극복하고 범용적인 분석 로직을 구축함.

향후 계획: 누적된 로그 데이터를 활용하여 메뉴별 소비 패턴 분석 AI 모델로 확장 예정.

6. 설치 및 실행 (Setup & Usage)

'''bash
# 저장소 복제
git clone (https://github.com/koonie404/Smart-Food-Inventory-System.git)

# 가상환경 설정 및 패키지 설치
pip install -r requirements.txt

# 시스템 실행
python main.py --source video.mp4


© 2026 임청수. All rights reserved. (임베디드 & 지능로봇 개발 과정)
