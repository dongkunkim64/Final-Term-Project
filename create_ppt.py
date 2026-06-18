import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def create_presentation():
    prs = Presentation()

    # 1. 표지 (Title Slide)
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "군용 무인자율차량(UGV)의 실시간 해킹 탐지를 위한\n경량화 AI 및 동형암호 결합 프레임워크"
    subtitle.text = "AI 프로그래밍 기말 프로젝트\n발표자: 김동건"

    # 2. 목차 (TOC)
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    
    title_shape.text = "목차 (Table of Contents)"
    tf = body_shape.text_frame
    tf.text = "1. 연구의 배경 (자율주행 보안 위협)"
    p = tf.add_paragraph()
    p.text = "2. 동형암호의 이론적 배경"
    p = tf.add_paragraph()
    p.text = "3. 경량화 AI 모델 선정 (Why Logistic Regression?)"
    p = tf.add_paragraph()
    p.text = "4. 실험 환경 구성 (Glows.ai 및 CARLA)"
    p = tf.add_paragraph()
    p.text = "5. 전반적인 실험 파이프라인"
    p = tf.add_paragraph()
    p.text = "6. 실험 결과 및 시연"
    p = tf.add_paragraph()
    p.text = "7. 결론"

    # 3. 연구의 배경
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "1. 연구의 배경"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "현대의 군사용 자율주행 차량(UGV)은 사이버 공격에 취약"
    p = tf.add_paragraph()
    p.text = "GPS 교란, 조향장치 탈취 등의 위협 존재"
    p = tf.add_paragraph()
    p.text = "아군 클라우드 서버조차 해킹될 수 있는 'Zero-Trust' 환경 대두"
    p = tf.add_paragraph()
    p.text = "해결책: 통신 감청과 서버 해킹을 원천 차단하는 '동형암호(FHE)' 도입"

    # 4. 동형암호 이론
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "2. 동형암호(FHE)의 이론적 배경"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "일반 암호화 = '잠긴 철제 금고'"
    p = tf.add_paragraph()
    p.text = "분석을 위해 반드시 금고를 열어야 함 (복호화 시 유출 위험)"
    p = tf.add_paragraph()
    p.text = "완전동형암호(FHE) = '장갑 낀 투명 금고'"
    p = tf.add_paragraph()
    p.text = "금고를 열지 않고도 내부 데이터를 조작 및 연산 가능"
    p = tf.add_paragraph()
    p.text = "수학적 준동형성: E(A) + E(B) = E(A+B)"
    p = tf.add_paragraph()
    p.text = "데이터 이동 및 연산 전 과정에서 완벽한 기밀성(0% 유출) 보장"

    # 5. 경량화 AI 모델
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "3. 경량화 AI 모델 선정 (Why Logistic Regression?)"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "최신 딥러닝(DNN) 적용의 한계"
    p = tf.add_paragraph()
    p.text = "비선형 함수 연산으로 인해 곱셈 횟수가 폭발하여 극도로 느려짐"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "로지스틱 회귀(Logistic Regression) 채택"
    p = tf.add_paragraph()
    p.text = "단순 선형 결합 구조로 곱셈 깊이(Multiplicative Depth) 최소화"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "초경량화 설계로 자율주행 방어 마지노선(100ms) 돌파"
    p.level = 1
    
    if os.path.exists('fhe_latency_comparison.png'):
        slide.shapes.add_picture('fhe_latency_comparison.png', Inches(4.5), Inches(2.5), width=Inches(5))

    # 6. 실험 환경
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "4. 실험 환경 구성"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "Glows.ai 고성능 클라우드 서버 활용"
    p = tf.add_paragraph()
    p.text = "CARLA 3D 물리 엔진 구동 및 대규모 데이터(10만 건) 추출"
    p = tf.add_paragraph()
    p.text = "데이터 분포 물리적 분석 (파란색: 정상 vs 빨간색: 해킹)"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "[정상] 속도 50km/h 및 조향각 0(직진) 유지 안전 주행"
    p.level = 2
    p = tf.add_paragraph()
    p.text = "[해킹] 속도 85km/h 이상 과속 및 핸들 급조작(조향각 0.8)"
    p.level = 2
    p = tf.add_paragraph()
    p.text = "AI가 이 물리적 패턴 차이를 학습하여 즉각적인 방어 수행"
    p.level = 1
    
    if os.path.exists('glowsai_animated_graph.gif'):
        slide.shapes.add_picture('glowsai_animated_graph.gif', Inches(4.5), Inches(2.0), width=Inches(5))

    # 7. 파이프라인
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "5. 전반적인 실험 파이프라인"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "1. 차량 (Client)"
    p = tf.add_paragraph()
    p.text = "CARLA 속 UGV 주행 데이터 수집 및 FHE 공개키 암호화"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "2. 클라우드 (Server)"
    p = tf.add_paragraph()
    p.text = "암호문을 풀지 않고 경량화 모델로 해킹 여부 고속 연산"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "3. 제어권 회수 (Client)"
    p = tf.add_paragraph()
    p.text = "결과 해독 후 해킹(1) 시 즉각 자율주행 제어권 강제 회수"
    p.level = 1

    # 8. 실험 결과
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "6. 실험 결과"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "정확도 (Accuracy)"
    p = tf.add_paragraph()
    p.text = "암호화 전/후 모두 96%의 완벽한 해킹 탐지 정확도 유지"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "실시간 방어 속도 (Latency)"
    p = tf.add_paragraph()
    p.text = "방대한 암호 연산에도 불구, 단 34.4ms(0.034초) 만에 탐지 완료"
    p.level = 1
    
    if os.path.exists('fhe_results_plot.png'):
        slide.shapes.add_picture('fhe_results_plot.png', Inches(4.5), Inches(2.5), width=Inches(5))

    # 9. 결론
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "7. 결론"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "본 프로젝트의 학술적/실무적 의의"
    p = tf.add_paragraph()
    p.text = "'완전동형암호'를 '초경량화 AI'와 결합하는 엔지니어링적 최적화 성공"
    p = tf.add_paragraph()
    p.text = "군용 작전 데이터의 '절대적 기밀성(보안)' 달성"
    p = tf.add_paragraph()
    p.text = "차량 사고를 방지하는 '실시간성(속도)' 증명"
    p = tf.add_paragraph()
    p.text = "미래 자율주행 무기체계의 근본적인 사이버 방어 가이드라인 제시"

    prs.save('UGV_FHE_Presentation.pptx')
    print("PPT 파일 'UGV_FHE_Presentation.pptx' 생성 완료!")

if __name__ == '__main__':
    create_presentation()
