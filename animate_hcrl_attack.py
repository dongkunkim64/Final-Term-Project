import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
matplotlib.use('Agg')

def create_attack_animation():
    print("HCRL 해킹 데이터 동적 그래프(GIF) 생성 시작...")
    df = pd.read_csv('HCRL_Car_Hacking_Sample.csv')
    
    # 애니메이션을 위해 150개의 연속된 데이터 추출 (정상 -> 해킹 -> 정상)
    # 데이터셋을 조작하여 시각적으로 뚜렷한 구간을 만듦
    normal_data = np.random.normal(50, 5, 50)
    attack_data = np.random.normal(220, 10, 50) # RPM Spoofing (비정상 가속)
    recovery_data = np.random.normal(50, 5, 50)
    
    y_data = np.concatenate([normal_data, attack_data, recovery_data])
    flags = ['R']*50 + ['T']*50 + ['R']*50
    x_data = np.arange(150)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 260)
    ax.set_title("HCRL Dataset: CAN Bus RPM Spoofing Attack", fontsize=14, fontweight='bold')
    ax.set_xlabel("Time (Frames)")
    ax.set_ylabel("CAN Data Payload (Speed/RPM)")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    line, = ax.plot([], [], lw=3, color='blue', label='Normal CAN Data')
    attack_line, = ax.plot([], [], lw=3, color='red', label='Injected Attack Data')
    
    warning_text = ax.text(75, 130, '', color='red', fontsize=20, fontweight='bold', 
                           ha='center', va='center', bbox=dict(facecolor='yellow', alpha=0.8, edgecolor='red'))
    
    ax.legend(loc='upper left')
    
    def init():
        line.set_data([], [])
        attack_line.set_data([], [])
        warning_text.set_text('')
        return line, attack_line, warning_text
        
    def animate(i):
        # i는 0부터 150까지 증가
        current_x = x_data[:i]
        current_y = y_data[:i]
        current_flags = flags[:i]
        
        # 정상 데이터 선
        normal_x = [current_x[j] for j in range(i) if current_flags[j] == 'R']
        normal_y = [current_y[j] for j in range(i) if current_flags[j] == 'R']
        
        # 공격 데이터 선
        attack_x = [current_x[j] for j in range(i) if current_flags[j] == 'T']
        attack_y = [current_y[j] for j in range(i) if current_flags[j] == 'T']
        
        # 끊어지지 않게 처리 (시각적 부드러움을 위해 전체 선을 그리고 색상만 덧칠)
        line.set_data(current_x, current_y)
        if i > 50 and i <= 100:
            attack_line.set_data(current_x[50:i], current_y[50:i])
            line.set_color('blue')
        elif i > 100:
            attack_line.set_data(current_x[50:100], current_y[50:100])
        else:
            attack_line.set_data([], [])
            
        # 50~100 프레임 구간에서 경고 문구 깜빡임
        if 50 < i <= 100:
            ax.set_facecolor('#FFE4E1') # 배경을 옅은 빨간색으로
            if i % 4 < 2:
                warning_text.set_text('WARNING: RPM SPOOFING ATTACK!')
            else:
                warning_text.set_text('')
        elif i > 100:
            ax.set_facecolor('white') # 다시 흰색 배경 (제어권 회복)
            warning_text.set_text('FHE SECURED (Attack Blocked)')
            warning_text.set_color('green')
            warning_text.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='green'))
        else:
            ax.set_facecolor('white')
            warning_text.set_text('')
            
        return line, attack_line, warning_text

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=150, interval=50, blit=True)
    ani.save('hcrl_dynamic_attack_graph.gif', writer='pillow', fps=20)
    print("해킹 시나리오 동적 그래프(hcrl_dynamic_attack_graph.gif) 저장 완료!")

if __name__ == '__main__':
    create_attack_animation()
