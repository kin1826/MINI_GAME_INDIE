# 🎮 2D Game Project – Python (Pygame)

## 📖 Giới thiệu

Đây là một dự án game 2D đơn giản được phát triển hoàn toàn bằng Python sử dụng thư viện Pygame.

Mục tiêu của project là luyện tập các kiến thức nền tảng trong lập trình game mà không sử dụng game engine như Unity hay Godot.

🔧 Tất cả logic trong game đều được xây dựng thủ công để hiểu sâu về cách game hoạt động bên trong.

---

## 🚀 Tính năng chính

- 🎮 Game loop chuẩn (update – render – event handling)

- ⌨️ Xử lý input từ bàn phím

- 💥 Hệ thống va chạm (collision detection)

- 🖼️ Rendering đối tượng lên màn hình

- 🕹️ Điều khiển nhân vật cơ bản

---

## 🛠️ Công nghệ sử dụng

- Python 3.x

- Pygame

- Lập trình thuần (không dùng game engine)

---

## 📂 Cấu trúc thư mục (gợi ý)

```bash
project/

├── src/
│   ├── main.py        # File chạy chính
│   ├── player.py      # Xử lý nhân vật
│   ├── enemy.py       # (tuỳ chọn) kẻ địch
│   ├── utils.py       # Hàm hỗ trợ

├── assets/            # Hình ảnh, âm thanh

├── README.md
└── requirements.txt
⚙️ Cài đặt & chạy project
1. Clone repository
git clone https://github.com/your-username/your-repo.git

cd your-repo
2. Cài thư viện
pip install pygame

Hoặc dùng file requirements:

pip install -r requirements.txt
3. Chạy game
python src/main.py
🎮 Điều khiển trong game
Phím	Chức năng
W A S D	Di chuyển
SPACE	Nhảy
ESC	Thoát game
🧠 Kiến thức áp dụng

Dự án này giúp bạn hiểu rõ:

Game loop hoạt động như thế nào
Xử lý sự kiện (event handling)
Vector & chuyển động trong game
Va chạm (collision detection)
Rendering frame-by-frame
🔮 Hướng phát triển thêm

Bạn có thể mở rộng project với:

🎞️ Animation (sprite sheet)
🔊 Âm thanh (sound effects, background music)
🗺️ Level system
🤖 AI cho enemy
💾 Save / Load game
🧩 UI (menu, pause, HUD)
📌 Mục đích

Project được xây dựng nhằm:

Học lập trình game từ nền tảng
Hiểu sâu cách engine hoạt động phía sau
Làm portfolio cá nhân
👨‍💻 Tác giả

Trần Văn Bằng
