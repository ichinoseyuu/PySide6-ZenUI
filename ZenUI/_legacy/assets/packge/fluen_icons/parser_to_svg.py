# parser_to_svg.py

import os

def save_icons_to_svg():
    """读取icons文件并保存为单独的svg文件"""
    try:
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 创建svg输出目录
        svg_output_dir = os.path.join(current_dir, 'svg_icons')
        if not os.path.exists(svg_output_dir):
            os.makedirs(svg_output_dir)
        
        # 读取icon文件
        icon_file = os.path.join(current_dir, 'fluent_ui_icon_regular.icons')
        
        # 读取并处理每一行
        with open(icon_file, 'r', encoding='utf-8') as file:
            for line in file:
                # 跳过注释和空行
                if line.startswith('##') or not line.strip():
                    continue
                    
                # 分离图标名称和数据
                line = line.strip()
                try:
                    icon_name, icon_data = line.split("////")
                    
                    # 替换颜色占位符
                    icon_data = icon_data.replace("<<<COLOR_CODE>>>", '#bfbfbf')
                    
                    # 构建svg文件路径
                    svg_file_path = os.path.join(svg_output_dir, f"{icon_name}.svg")
                    
                    # 保存svg文件
                    with open(svg_file_path, 'w', encoding='utf-8') as svg_file:
                        svg_file.write(icon_data)
                        
                    print(f"已保存: {icon_name}.svg")
                    
                except ValueError as e:
                    print(f"处理行时出错: {line}")
                    print(f"错误信息: {str(e)}")
                    continue

    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")

def main():
    print("开始将图标转换为SVG文件...")
    save_icons_to_svg()
    print("转换完成!")

if __name__ == "__main__":
    main()