import os
from PIL import Image
import concurrent.futures

def convert_tiff_to_jpg(tiff_path, jpg_path):
    """转换单个TIFF文件为JPG"""
    try:
        with Image.open(tiff_path) as img:
            # 转换为RGB模式（如果原来是RGBA或其他模式）
            if img.mode in ('RGBA', 'LA'):
                # 创建一个白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])  # 使用alpha通道作为mask
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 保存为JPG，可以调整质量（0-100）
            img.save(jpg_path, 'JPEG', quality=95)
            print(f"转换成功: {tiff_path} -> {jpg_path}")
            return True
    except Exception as e:
        print(f"转换失败 {tiff_path}: {e}")
        return False

def batch_convert_tiff_to_jpg(source_dir, target_dir):
    """批量转换TIFF到JPG"""
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)
    
    # 获取所有TIFF文件
    tiff_files = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.tiff', '.tif')):
                tiff_files.append(os.path.join(root, file))
    
    print(f"找到 {len(tiff_files)} 个TIFF文件")
    
    # 使用多线程加速转换
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for tiff_path in tiff_files:
            # 构建目标路径
            relative_path = os.path.relpath(tiff_path, source_dir)
            jpg_path = os.path.join(target_dir, os.path.splitext(relative_path)[0] + '.jpg')
            
            # 创建目标子目录（如果需要）
            os.makedirs(os.path.dirname(jpg_path), exist_ok=True)
            
            # 提交转换任务
            futures.append(executor.submit(convert_tiff_to_jpg, tiff_path, jpg_path))
        
        # 等待所有任务完成
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    success_count = sum(results)
    print(f"转换完成! 成功: {success_count}, 失败: {len(tiff_files) - success_count}")

# 使用示例
if __name__ == "__main__":
    source_dir = "./data/nyc/cropped_tiff"
    target_dir = "./data/nyc/cropped_jpg"
    
    batch_convert_tiff_to_jpg(source_dir, target_dir)