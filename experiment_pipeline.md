# 전반적인 실험 파이프라인 (Architecture Flow)

발표 슬라이드(PPT)에 캡처해서 넣을 수 있는 시스템 파이프라인 구조도입니다.

```mermaid
flowchart TD
    subgraph Client ["차량 내부 (UGV Client)"]
        A[CARLA 시뮬레이터\n주행 및 센서 데이터] -->|스피드, 조향, GPS| B(정규화 전처리\nStandardScaler)
        B --> C{FHE 암호화\n(Public Key)}
        
        G{FHE 복호화\n(Secret Key)} --> H{해킹 여부 판별}
        H -->|결과 = 0| I((정상 주행 유지))
        H -->|결과 = 1| J((긴급 제어권 회수\nHUD 경고 발생))
    end

    subgraph Server ["외부 클라우드 (AI Server)"]
        C -->|암호문 전송\n(통신 감청 불가)| D[암호 상태 연산\nHomomorphic Inference]
        E[(경량화 AI 모델\nLogistic Regression)] -.-> D
        D -->|결과 암호문 전송| G
    end

    classDef client fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef server fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef highlight fill:#ffebee,stroke:#c62828,stroke-width:2px;
    
    class A,B,C,G,H,I client;
    class D,E server;
    class J highlight;
```

---
**[다이어그램 활용법]**
위 다이어그램을 캡처하시거나, `mermaid` 지원 툴을 이용해 파워포인트에 붙여넣으시면 훌륭한 파이프라인 설명 도식화가 완성됩니다.
