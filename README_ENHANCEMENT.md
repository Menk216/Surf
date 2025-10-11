# 🎮 Fantascy Suffer - Game Enhancement

## ✨ Tính năng mới đã được thêm vào

### 🌅🌙 Hệ thống Theme động
- **Chuyển đổi tự động**: Game tự động chuyển đổi giữa giao diện sáng (Ngày) và tối (Đêm) mỗi 15 giây
- **Hiệu ứng chuyển đổi**: Có hiệu ứng fade và particles khi chuyển theme
- **Theme đêm**: 
  - Màu nền tối hơn với hiệu ứng sao lấp lánh
  - Mặt trăng với các phase khác nhau
  - Ánh sáng ambient giảm để tạo cảm giác đêm
- **Theme ngày**:
  - Màu sắc tươi sáng, rực rỡ
  - Ánh sáng ambient cao
  - Hiệu ứng sóng nước mạnh mẽ hơn

### 🎨 UI/UX được cải thiện
- **Panel điểm số đẹp mắt**:
  - Gradient background với hiệu ứng glow
  - Icon ngôi sao cho điểm số
  - Icon đồng xu cho coins
  - Hiệu ứng pulse và sparkle
- **Nút điều khiển**: Đã được đơn giản hóa
- **Chỉ báo theme**: Hiển thị theme hiện tại và tiến độ chuyển đổi


## 🚀 Cách chạy game

1. **Cài đặt dependencies**:
```bash
pip install pygame
```

2. **Chạy game**:
```bash
python main.py
```

## 📁 Cấu trúc file mới

```
├── theme_manager.py          # Quản lý theme sáng/tối
├── ui_manager.py             # Quản lý UI và hiệu ứng
├── screens/
│   ├── play.py              # Màn chơi chính (đã cập nhật)
│   ├── entities.py          # Entities (đã cập nhật)
│   └── ...
└── ...
```

## 🎮 Cách chơi

- **Di chuyển**: Di chuyển chuột để điều khiển player
- **Thu thập**: Ăn coins để tăng điểm và coins
- **Tránh**: Tránh obstacles và monsters
- **Theme**: Quan sát sự chuyển đổi theme mỗi 15 giây

## 🔧 Tùy chỉnh

### Thay đổi thời gian chuyển theme:
Trong `theme_manager.py`:
```python
self.theme_duration = 15000  # Thay đổi từ 15 giây
```


### Thay đổi màu sắc theme:
Trong `theme_manager.py`, chỉnh sửa dictionary `themes`

## 🎨 Tính năng visual

- **Gradient backgrounds**: Tất cả UI elements sử dụng gradient
- **Glow effects**: Hiệu ứng ánh sáng cho buttons
- **Particle systems**: Hiệu ứng particles khi chuyển theme
- **Smooth animations**: Tất cả animations đều mượt mà
- **Responsive design**: UI tự động điều chỉnh theo theme

## 🐛 Debugging

Nếu gặp lỗi:
1. Kiểm tra file paths trong code
2. Đảm bảo tất cả assets tồn tại
3. Kiểm tra pygame version compatibility

## 🔮 Tính năng có thể phát triển thêm

- **Sound effects**: Thêm âm thanh cho theme changes
- **Achievements**: Hệ thống thành tích
- **Leaderboard**: Bảng xếp hạng
- **Settings menu**: Menu cài đặt chi tiết
- **Save/Load**: Lưu tiến độ game

---

**Chúc bạn chơi game vui vẻ! 🎉**
