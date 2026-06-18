from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
import os

def create_presentation():
    prs = Presentation()

    # 슬라이드 레이아웃 설정
    title_slide_layout = prs.slide_layouts[0]
    bullet_slide_layout = prs.slide_layouts[1]

    # 1. 표지
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "자율주행 무인차량(UGV)의 사이버 해킹 방어를 위한\n동형암호(FHE) 기반 초경량 이상탐지 시스템"
    subtitle.text = "기말 프로젝트 최종 발표\n발표자: 김동건"

    # 2. 목차
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "발표 순서"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "1. 연구 배경 및 문제 정의"
    p = tf.add_paragraph()
    p.text = "2. 동형암호(FHE) 이론 및 적용"
    p = tf.add_paragraph()
    p.text = "3. 경량화 AI(로지스틱 회귀) 선정 이유"
    p = tf.add_paragraph()
    p.text = "4. 시스템 아키텍처 및 파이프라인"
    p = tf.add_paragraph()
    p.text = "5. 구현 시도 및 기술적 한계 (Challenges)"
    p = tf.add_paragraph()
    p.text = "6. 향후 과제 (Future Work) 및 결론"

    # 3. 연구 배경
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "1. 연구 배경 및 문제 정의"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "현대 군사 작전에서 무인차량(UGV)의 중요성 증대"
    p = tf.add_paragraph()
    p.text = "적군의 악의적인 해킹(속도 급가속, 조향각 조작) 위협 존재"
    p = tf.add_paragraph()
    p.text = "기존 방어 방식의 한계"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "암호화된 데이터를 복호화하여 검사하는 동안 지연 시간 발생"
    p.level = 2
    p = tf.add_paragraph()
    p.text = "해킹당할 경우 아군에게 치명적인 피해 발생 가능"
    p.level = 2

    # 4. 동형암호 이론
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "2. 동형암호(FHE) 이론 및 적용"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "동형암호(Fully Homomorphic Encryption)란?"
    p = tf.add_paragraph()
    p.text = "데이터를 암호화한 상태 그대로 연산할 수 있는 차세대 암호 기술"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "비유: '장갑이 부착된 투명 금고'"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "본 프로젝트의 적용 방안"
    p.level = 0
    p = tf.add_paragraph()
    p.text = "UGV의 센서 데이터를 암호화하여 클라우드로 전송"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "서버는 복호화 없이 AI 모델로 이상 여부 판단 후 암호문 반환"
    p.level = 1

    # 5. 로지스틱 회귀 선정 이유
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "3. 경량화 AI 선정 이유"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "자율주행의 핵심은 '실시간성(Low Latency)'"
    p = tf.add_paragraph()
    p.text = "DNN 등 복잡한 모델 적용 시도 및 한계"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "비선형 함수(ReLU/Sigmoid) 처리 시 연산 과부하 발생 (850ms~3,400ms)"
    p.level = 2
    p = tf.add_paragraph()
    p.text = "초경량 로지스틱 회귀(Logistic Regression) 도입"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "단순 선형 연산으로 오버헤드 최소화 (처리속도 34.4ms 달성)"
    p.level = 2
    
    if os.path.exists('fhe_latency_comparison.png'):
        slide.shapes.add_picture('fhe_latency_comparison.png', Inches(4.5), Inches(2.0), width=Inches(5))

    # 6. 시스템 파이프라인
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "4. 시스템 아키텍처 및 파이프라인"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "Client (UGV 차량)"
    p = tf.add_paragraph()
    p.text = "센서 데이터 수집 ➡️ 정규화 ➡️ 공개키 암호화 ➡️ 서버 전송"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "서버로부터 수신한 암호문 해독 ➡️ 해킹 여부 판단 ➡️ 비상 제동"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Server (클라우드)"
    p.level = 0
    p = tf.add_paragraph()
    p.text = "암호화된 데이터 수신 ➡️ 로지스틱 회귀 추론 ➡️ 암호문 반환"
    p.level = 1

    # 7. 구현 시도 및 기술적 한계 (New)
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "5. 구현 시도 및 기술적 한계 (Challenges)"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "Glows.ai 서버를 활용한 CARLA 3D 물리 시뮬레이션 환경 구축 시도"
    p = tf.add_paragraph()
    p.text = "직면한 시스템적/환경적 제약사항"
    p.level = 0
    p = tf.add_paragraph()
    p.text = "서버 컨테이너 권한 제약 (systemd 미지원으로 인한 Docker 실행 불가)"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "CARLA 공식 S3 배포 서버 접근 차단으로 인한 Native 설치 실패"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "결과적으로 해당 서버 환경에서의 실제 3D 물리 검증은 불가했음"
    p.level = 1

    # 8. 향후 과제
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "6. 향후 과제 (Future Work)"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "로컬 PC 또는 완전한 가상머신(EC2 등) 환경으로 마이그레이션"
    p = tf.add_paragraph()
    p.text = "실제 CARLA 3D 엔진 구동을 통한 10만 건 이상의 주행 데이터 추출"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "추출된 데이터(정상/해킹)를 바탕으로 로지스틱 회귀 모델 최종 학습"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "실차(RC카 등) 환경을 구축하여 하드웨어 통합 테스트(HIL) 진행"
    p.level = 1

    # 9. 결론
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "결론"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "동형암호는 군사 보안의 핵심 기술로 발전할 것"
    p = tf.add_paragraph()
    p.text = "자율주행에 동형암호를 적용하기 위해서는 '로지스틱 회귀'와 같은 초경량화 모델이 필수적임을 이론적으로 증명함"
    p = tf.add_paragraph()
    p.text = "비록 시뮬레이션 검증 환경 구축에는 실패하였으나, 엔지니어링 한계를 극복하기 위한 인사이트 도출"

    prs.save('UGV_FHE_Presentation_Honest.pptx')
    print("정직한 서사의 PPT 파일 'UGV_FHE_Presentation_Honest.pptx' 생성 완료!")

if __name__ == '__main__':
    create_presentation()
