# Import các thư viện cần thiết
import cv2
from pyzbar.pyzbar import decode
import qrcode   
import os

# Hàm để giải mã mã vạch từ một hình ảnh cho trước
def docMaVach(image):
    # Đọc hình ảnh thành mảng numpy sử dụng cv2
    img = cv2.imread(image)

    # Giải mã hình ảnh mã vạch
    detectedBarcodes = decode(img)

    # Nếu không tìm thấy mã vạch, in thông báo
    if not detectedBarcodes:
        print(f"Không thể giải mã mã vạch từ hình ảnh {image} hoặc mã vạch của bạn không rõ ràng!")
        return None

    danhSachDuLieuMaVach = []
    danhSachLoaiMaVach = []  # Danh sách để lưu trữ các loại mã vạch

    # Tạo thư mục đầu ra cho mã QR nếu nó chưa tồn tại
    thuMucQRCode = "qrcode"
    os.makedirs(thuMucQRCode, exist_ok=True)

    # Tạo thư mục đầu ra cho mã vạch nếu nó chưa tồn tại
    thuMucMaVach = "barcode"
    os.makedirs(thuMucMaVach, exist_ok=True)

    # Duyệt qua tất cả các mã vạch được tìm thấy trong hình ảnh
    for barcode in detectedBarcodes:
        # Xác định vị trí mã vạch trong hình ảnh
        (x, y, w, h) = barcode.rect

        # Vẽ hình chữ nhật trên hình ảnh để làm nổi bật mã vạch
        cv2.rectangle(img, (x-10, y-10),
                      (x + w+10, y + h+10),
                      (255, 0, 0), 2)

        if barcode.data != "":
            # In thông tin dữ liệu mã vạch và loại mã vạch
            duLieuMaVach = barcode.data.decode("utf-8")
            loaiMaVach = barcode.type
            print(f"Dữ liệu mã vạch: {duLieuMaVach}")
            print(f"Loại mã vạch: {loaiMaVach}")
            danhSachDuLieuMaVach.append(duLieuMaVach)
            danhSachLoaiMaVach.append(loaiMaVach)

            # Tạo mã QR cho dữ liệu mã vạch
            qr = qrcode.QRCode(version=10,
                              error_correction=qrcode.constants.ERROR_CORRECT_H,
                              box_size=20,
                              border=3)
            qr.add_data(duLieuMaVach)
            qr.make(fit=True)

            # Lưu hình ảnh mã QR
            tenTepQRCode = f"qrcode_{duLieuMaVach}_{loaiMaVach}.png"
            duongDanQRCode = os.path.join(thuMucQRCode, tenTepQRCode)
            hinhAnhQRCode = qr.make_image(fill_color="darkblue", back_color="white")
            hinhAnhQRCode.save(duongDanQRCode)

            # Lưu hình ảnh mã vạch
            tenTepMaVach = f"barcode_{duLieuMaVach}_{loaiMaVach}.png"
            duongDanMaVach = os.path.join(thuMucMaVach, tenTepMaVach)
            cv2.imwrite(duongDanMaVach, img)

    # Hiển thị hình ảnh với các mã vạch đã tìm thấy
    cv2.imshow("Hình ảnh", img)
    cv2.waitKey(0)

    return danhSachDuLieuMaVach, danhSachLoaiMaVach

# Hàm kiểm tra xem tệp có tồn tại trong thư mục làm việc hiện tại hay không
def kiemTraTep(imagefile):
    # Lấy thư mục làm việc hiện tại
    thuMucHienTai = os.getcwd()
    # Kết hợp thủa mục hiện tại với tên tệp
    duongDan = os.path.join(thuMucHienTai, imagefile)

    # Kiểm tra xem đường dẫn đã cho có tồn tại hay không
    tonTai = os.path.exists(duongDan)
    return tonTai

if __name__ == "__main__":
    # Nhập tên tệp hình ảnh chứa mã vạch từ người dùng và gán cho biến imagefile
    imagefile = input("Nhập tên tệp hình ảnh chứa mã vạch: ")
    print(f"Tên tệp mà bạn đã nhập là: {imagefile}")

    # Kiểm tra xem tệp hình ảnh có tồn tại trong thư mục làm việc hiện tại hay không
    kiemTraTonTai = kiemTraTep(imagefile)

    # Nếu tệp hình ảnh tồn tại, thì giải mã hình ảnh
    if kiemTraTonTai:
        danhSachDuLieuMaVach, danhSachLoaiMaVach = docMaVach(imagefile)

        # Kiểm tra dữ liệu mã vạch để tạo mã QR
        if danhSachDuLieuMaVach:
            print("Đã tạo mã QR thành công.")
            for duLieuMaVach, loaiMaVach in zip(danhSachDuLieuMaVach, danhSachLoaiMaVach):
                print(f"Dữ liệu mã vạch: {duLieuMaVach}")
                print(f"Loại mã vạch: {loaiMaVach}")
        else:
            print('Không tìm thấy mã vạch nào trong hình ảnh!')
    else:
        print(f'Không tìm thấy tệp {imagefile} trong thư mục này')

    # Đóng tất cả cửa sổ được tạo ra bằng cv2.destroyAllWindows()
    cv2.destroyAllWindows()