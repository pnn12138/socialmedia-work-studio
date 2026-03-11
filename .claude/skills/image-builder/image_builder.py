#!/usr/bin/env python3
"""
Image Builder - 图像生成流程编排脚本

整合视觉规划、素材检索、图像合成、导出质检的端到端流程

依赖：
- pillow
- opencv-python
- requests
- python-dotenv
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 加载根目录 .env 文件
try:
    from dotenv import load_dotenv
    # 查找根目录.env 文件
    def find_root_env():
        """向上查找根目录的.env 文件"""
        current = Path(__file__).resolve()
        # 向上查找 5 层
        for _ in range(5):
            current = current.parent
            env_path = current / '.env'
            if env_path.exists():
                return env_path
        return None

    root_env = find_root_env()
    if root_env:
        load_dotenv(dotenv_path=root_env)
except ImportError:
    pass  # python-dotenv 未安装则跳过

# 导入本地模块
try:
    from image_compose import process_image, create_quote_card, compare_images
    from smart_cropper import smart_crop_pil, analyze_image
except ImportError:
    print("Error: Cannot import local modules. Make sure image_compose.py and smart_cropper.py are in the same directory.")
    sys.exit(1)

try:
    from PIL import Image
    import requests
except ImportError as e:
    print(f"Error: Missing dependency. Please run: pip install {str(e).split()[-1]}")
    sys.exit(1)


class ImageBuilder:
    """图像生成流程编排器"""

    def __init__(self, topic_name, output_dir=None):
        """
        初始化图像生成器

        Args:
            topic_name: 选题名称
            output_dir: 输出目录，默认为 topics/{topic_name}/fig/定稿图/
        """
        self.topic_name = topic_name

        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(f"topics/{topic_name}/fig/定稿图")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 素材目录
        self素材_dir = Path(f"topics/{topic_name}/fig/原始素材")
        self.素材_dir.mkdir(parents=True, exist_ok=True)

        # 执行日志
        self.build_log = []

    def log(self, message, level="info"):
        """记录日志"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
        }
        self.build_log.append(entry)
        print(f"[{level.upper()}] {message}")

    def load_visual_plan(self, visual_plan_path):
        """
        加载视觉规划方案

        Args:
            visual_plan_path: visual_plan.md 或 requirements.md 路径

        Returns:
            解析后的执行方案
        """
        if not Path(visual_plan_path).exists():
            raise FileNotFoundError(f"Visual plan not found: {visual_plan_path}")

        # 这里简化处理，实际需要解析 markdown 或 JSON
        # 假设 visual_plan.md 中包含 JSON 格式的执行方案
        with open(visual_plan_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 尝试提取 JSON
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))

        # 如果没有 JSON，返回原始内容
        return {"raw": content}

    def download_material(self, url, save_path):
        """
        下载素材

        Args:
            url: 素材 URL
            save_path: 保存路径
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)

            self.log(f"Downloaded: {url} -> {save_path}")
            return True
        except Exception as e:
            self.log(f"Failed to download {url}: {e}", level="error")
            return False

    def process_image_by_plan(self, image_plan):
        """
        按单张图片计划执行

        Args:
            image_plan: 单张图片的执行计划

        Returns:
            输出文件路径
        """
        image_id = image_plan.get("id", "unknown")
        purpose = image_plan.get("purpose", "")
        source_mode = image_plan.get("source_mode", "existing")
        post_process_plan = image_plan.get("post_process_plan", [])

        self.log(f"Processing {image_id}: {purpose}")

        # 根据 source_mode 选择执行路径
        if source_mode == "existing":
            # 使用现有素材
            source_file = image_plan.get("source_file")
            if not source_file or not Path(source_file).exists():
                self.log(f"Source file not found: {source_file}", level="error")
                return None

            output_path = self.output_dir / f"{image_id}.png"
            process_image(source_file, str(output_path), post_process_plan)
            return str(output_path)

        elif source_mode == "hybrid-edit":
            # 混合编辑（素材裁剪拼接 + 加字）
            source_file = image_plan.get("source_file")
            if not source_file or not Path(source_file).exists():
                self.log(f"Source file not found: {source_file}", level="error")
                return None

            # 先智能裁剪
            ratio = image_plan.get("ratio", "3:4")
            cropped_path = self.素材_dir / f"{image_id}_cropped.png"

            from smart_cropper import smart_crop_pil
            from PIL import Image

            image = Image.open(source_file)
            from image_compose import parse_ratio
            cropped = smart_crop_pil(image, parse_ratio(ratio), focus="auto")
            cropped.save(str(cropped_path))

            # 再执行后处理
            output_path = self.output_dir / f"{image_id}.png"
            post_process_plan.insert(0, {
                "type": "resize",
                "width": image_plan.get("output_width", 1080),
                "height": image_plan.get("output_height", 1440),
            })
            process_image(str(cropped_path), str(output_path), post_process_plan)
            return str(output_path)

        elif source_mode == "quote-card":
            # 引用卡片
            quote = image_plan.get("quote", "")
            author = image_plan.get("author", "")
            background = image_plan.get("background")
            style = image_plan.get("style", "minimalist")
            output_size = image_plan.get("output_size", (1080, 1080))

            output_path = self.output_dir / f"{image_id}.png"
            result = create_quote_card(quote, author, background, style, output_size)
            result.save(str(output_path))
            return str(output_path)

        elif source_mode == "comparison":
            # 对比图
            image1 = image_plan.get("image1")
            image2 = image_plan.get("image2")
            labels = image_plan.get("labels", ("Before", "After"))
            orientation = image_plan.get("orientation", "horizontal")

            output_path = self.output_dir / f"{image_id}.png"
            result = compare_images(image1, image2, labels, orientation)
            result.save(str(output_path))
            return str(output_path)

        elif source_mode == "ai-generate" or source_mode == "external-ai":
            # AI 生成（需要外部调用，这里只做记录）
            self.log(f"AI generation required for {image_id}. Prompt: {image_plan.get('prompt', 'N/A')}", level="warning")
            self.log("Please generate image externally and provide the file.", level="warning")
            return None

        else:
            self.log(f"Unknown source_mode: {source_mode}", level="error")
            return None

    def execute(self, visual_plan_path):
        """
        执行完整的图像生成流程

        Args:
            visual_plan_path: 视觉规划文件路径

        Returns:
            执行结果
        """
        self.log(f"Starting image build for topic: {self.topic_name}")

        # 加载视觉规划
        plan = self.load_visual_plan(visual_plan_path)

        # 获取图片执行列表
        images_plan = plan.get("images", [])

        if not images_plan:
            self.log("No images to process in visual plan", level="warning")
            return {"success": False, "message": "No images to process"}

        # 逐张处理
        results = {}
        for image_plan in images_plan:
            output_path = self.process_image_by_plan(image_plan)
            image_id = image_plan.get("id", "unknown")
            results[image_id] = {
                "success": output_path is not None,
                "output_path": output_path,
            }

        # 保存执行日志
        self.save_build_log()

        # 总结
        success_count = sum(1 for r in results.values() if r["success"])
        total_count = len(results)

        self.log(f"Completed: {success_count}/{total_count} images")

        return {
            "success": success_count == total_count,
            "results": results,
            "log_path": str(self.output_dir / "build-log.json"),
        }

    def save_build_log(self):
        """保存执行日志"""
        log_path = self.output_dir / "build-log.json"
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.build_log, f, ensure_ascii=False, indent=2)
        self.log(f"Build log saved to: {log_path}")


def main():
    parser = argparse.ArgumentParser(description="Image Builder - 图像生成流程编排")
    parser.add_argument("topic", help="选题名称")
    parser.add_argument("--plan", required=True, help="视觉规划文件路径 (visual_plan.md)")
    parser.add_argument("--output-dir", help="输出目录")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不执行")

    args = parser.parse_args()

    if args.dry_run:
        print(f"=== DRY RUN MODE ===")
        print(f"Topic: {args.topic}")
        print(f"Plan: {args.plan}")
        print(f"Output: {args.output_dir or 'topics/{topic}/fig/定稿图/'}")
        print("\nThis will process images according to the visual plan.")
        return

    builder = ImageBuilder(args.topic, args.output_dir)
    result = builder.execute(args.plan)

    if result["success"]:
        print("\n✅ Image build completed successfully!")
    else:
        print("\n⚠️  Image build completed with some failures.")
        for image_id, r in result["results"].items():
            if not r["success"]:
                print(f"  - {image_id}: FAILED")

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
