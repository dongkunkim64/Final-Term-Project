import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
matplotlib.use('Agg')

def create_validation_animation():
    print("FHE 검증 동적 그래프(GIF) 생성 시작...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle('FHE Logistic Regression Validation on HCRL Dataset', fontsize=16, fontweight='bold')
    
    # 목표 데이터
    labels_acc = ['Plaintext', 'FHE (Encrypted)']
    target_acc = [79.53, 79.00]
    
    labels_lat = ['FHE Inference']
    target_lat = [2.47]
    target_threshold = 34.4
    
    # 막대 그래프 초기화
    bars_acc = ax1.bar(labels_acc, [0, 0], color=['gray', 'blue'])
    ax1.set_ylim(0, 100)
    ax1.set_ylabel('Accuracy (%)', fontsize=12)
    ax1.set_title('Detection Accuracy Comparison', fontsize=14)
    
    bars_lat = ax2.bar(labels_lat, [0], color=['green'])
    ax2.set_ylim(0, 50)
    ax2.set_ylabel('Latency (ms)', fontsize=12)
    ax2.set_title('Average Inference Latency', fontsize=14)
    
    # 목표 지연시간 점선
    threshold_line = ax2.axhline(y=target_threshold, color='red', linestyle='--', alpha=0)
    
    # 텍스트 레이블 초기화
    texts_acc = [ax1.text(bar.get_x() + bar.get_width()/2, 0, '', ha='center', va='bottom', fontweight='bold', fontsize=12) for bar in bars_acc]
    texts_lat = [ax2.text(bars_lat[0].get_x() + bars_lat[0].get_width()/2, 0, '', ha='center', va='bottom', fontweight='bold', fontsize=12)]
    threshold_text = ax2.text(0, target_threshold+1, 'Target (< 34.4 ms)', color='red', fontweight='bold', alpha=0)
    
    def init():
        for bar in bars_acc:
            bar.set_height(0)
        for bar in bars_lat:
            bar.set_height(0)
        for text in texts_acc + texts_lat:
            text.set_text('')
        threshold_line.set_alpha(0)
        threshold_text.set_alpha(0)
        return list(bars_acc) + list(bars_lat) + texts_acc + texts_lat + [threshold_line, threshold_text]
        
    def animate(i):
        # 60프레임 동안 애니메이션
        progress = min(i / 40.0, 1.0)
        
        # 정확도 바 성장
        for j, bar in enumerate(bars_acc):
            current_h = target_acc[j] * progress
            bar.set_height(current_h)
            if i > 5:
                texts_acc[j].set_position((bar.get_x() + bar.get_width()/2, current_h + 1))
                texts_acc[j].set_text(f'{current_h:.1f}%')
                
        # 레이턴시 바 성장 (i > 20부터 시작)
        if i > 20:
            lat_progress = min((i - 20) / 30.0, 1.0)
            current_l = target_lat[0] * lat_progress
            bars_lat[0].set_height(current_l)
            texts_lat[0].set_position((bars_lat[0].get_x() + bars_lat[0].get_width()/2, current_l + 1))
            texts_lat[0].set_text(f'{current_l:.2f} ms')
            
            # 목표선 서서히 나타남
            alpha_line = min((i - 20) / 20.0, 1.0)
            threshold_line.set_alpha(alpha_line)
            threshold_text.set_alpha(alpha_line)
            
        return list(bars_acc) + list(bars_lat) + texts_acc + texts_lat + [threshold_line, threshold_text]

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=80, interval=50, blit=True)
    ani.save('fhe_hcrl_validation_animated.gif', writer='pillow', fps=20)
    print("FHE 검증 동적 막대그래프(fhe_hcrl_validation_animated.gif) 저장 완료!")

if __name__ == '__main__':
    create_validation_animation()
