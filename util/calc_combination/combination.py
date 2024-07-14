import random

# Danh sách các sản phẩm mẫu
products = [
    "Ketchup", "Shaving Cream", "Light Bulb", "Ice Cream", "Milk",
    "Olive Oil", "Bread", "Spinach", "Tissues", "Mustard", "Dish Soap"
    # Thêm các sản phẩm khác nếu cần
]

# Số lượng tổ hợp cần tạo
num_combinations = 24000

# Danh sách để lưu trữ các tổ hợp
combinations = []

# Tạo 24000 tổ hợp ngẫu nhiên
for _ in range(num_combinations):
    # Chọn ngẫu nhiên số lượng sản phẩm từ 3 đến len(products)
    num_products = random.randint(3, len(products))
    # Chọn ngẫu nhiên các sản phẩm từ danh sách products
    selected_products = random.sample(products, num_products)
    # Ghép lại thành một chuỗi và thêm vào danh sách tổ hợp
    combination = ", ".join(selected_products)
    combinations.append(combination)

# Tên file để lưu trữ
file_name = "./24000_combinations.txt"

# Mở file để ghi vào chế độ văn bản
with open(file_name, 'w', encoding='utf-8') as file:
    for combination in combinations:
        file.write(combination + "\n")  # Ghi từng tổ hợp vào file, mỗi tổ hợp trên một dòng

print(f"Đã tạo thành công {num_combinations} tổ hợp và lưu vào file {file_name}")
