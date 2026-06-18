import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_diagram():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')

    # 메인 CAN Bus 라인
    ax.add_patch(patches.Rectangle((0.1, 0.45), 0.8, 0.1, color='lightblue', zorder=1))
    ax.text(0.5, 0.5, "Vehicle CAN Bus Network (KIA Soul)", fontsize=14, fontweight='bold', ha='center', va='center', zorder=2)

    # ECUs (정상 노드)
    ecus = [
        (0.15, 0.7, "Engine ECU\n(RPM)"),
        (0.4, 0.7, "Brake ECU"),
        (0.65, 0.7, "Steering ECU")
    ]
    for x, y, text in ecus:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.15, 0.15, boxstyle="round,pad=0.05", color='lightgreen', ec='green', lw=2))
        ax.text(x + 0.075, y + 0.075, text, fontsize=11, ha='center', va='center', fontweight='bold')
        # 연결선
        ax.plot([x + 0.075, x + 0.075], [y, 0.55], color='gray', lw=3, linestyle='--')

    # Hacker Node (공격 주입)
    ax.add_patch(patches.FancyBboxPatch((0.25, 0.1), 0.2, 0.15, boxstyle="round,pad=0.05", color='salmon', ec='red', lw=2))
    ax.text(0.35, 0.175, "Hacker Device\n(OBD-II Port)", fontsize=11, ha='center', va='center', fontweight='bold')
    
    # 공격 벡터 화살표
    ax.annotate("Injected Attacks\n(DoS, Fuzzy, Spoofing)", xy=(0.35, 0.45), xytext=(0.35, 0.25),
                arrowprops=dict(facecolor='red', shrink=0.05, width=3, headwidth=10),
                fontsize=10, ha='center', va='bottom', color='darkred', fontweight='bold')

    # 데이터셋 수집기
    ax.add_patch(patches.FancyBboxPatch((0.6, 0.1), 0.25, 0.15, boxstyle="round,pad=0.05", color='gold', ec='orange', lw=2))
    ax.text(0.725, 0.175, "Dataset Logger\n(Raspberry Pi)", fontsize=11, ha='center', va='center', fontweight='bold')
    
    # 수집 화살표
    ax.annotate("Extract Normal &\nAttack Traffic", xy=(0.725, 0.45), xytext=(0.725, 0.25),
                arrowprops=dict(facecolor='orange', shrink=0.05, width=3, headwidth=10),
                fontsize=10, ha='center', va='bottom', color='black', fontweight='bold')

    # 제목
    plt.title("HCRL Car Hacking Dataset Generation Architecture", fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('hcrl_dataset_architecture.png', dpi=300)
    print("HCRL 데이터셋 아키텍처 다이어그램 'hcrl_dataset_architecture.png' 생성 완료!")

if __name__ == '__main__':
    draw_diagram()
