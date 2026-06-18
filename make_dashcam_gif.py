from PIL import Image

# 이미지 경로
img1 = '/Users/dongkun/.gemini/antigravity/brain/4105df2d-6e8f-4271-a56d-b435de9b33c7/carla_normal_1781811948703.png'
img2 = '/Users/dongkun/.gemini/antigravity/brain/4105df2d-6e8f-4271-a56d-b435de9b33c7/carla_hacked_1781811960077.png'
img3 = '/Users/dongkun/.gemini/antigravity/brain/4105df2d-6e8f-4271-a56d-b435de9b33c7/carla_secured_1781811973584.png'

try:
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    i3 = Image.open(img3)
    
    # 리사이즈 (크기 통일)
    size = (800, 800)
    i1 = i1.resize(size)
    i2 = i2.resize(size)
    i3 = i3.resize(size)
    
    # GIF 저장 (각 프레임 1.5초 유지)
    i1.save('carla_3d_dashcam_simulation.gif',
            save_all=True,
            append_images=[i2, i3],
            duration=1500,
            loop=0)
    print("3D Dashcam GIF (carla_3d_dashcam_simulation.gif) 생성 완료!")
except Exception as e:
    print(f"GIF 생성 중 오류: {e}")
