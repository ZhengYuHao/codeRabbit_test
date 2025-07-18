
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Optional

class ImageCrawler:
    def __init__(self, save_dir: str = "downloaded_images"):
        """
        初始化图片爬虫
        
        Args:
            save_dir: 保存图片的目录路径
        """
        self.save_dir = save_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # 创建保存目录
        os.makedirs(self.save_dir, exist_ok=True)

    def get_page_content(self, url: str) -> Optional[str]:
        """
        获取页面HTML内容
        
        Args:
            url: 目标网页URL
            
        Returns:
            str: 页面HTML内容 或 None（失败时）
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"获取页面失败: {e}")
            return None

    def extract_image_urls(self, url: str, html_content: str) -> List[str]:
        """
        提取页面中的所有图片URL
        
        Args:
            url: 当前页面URL
            html_content: 页面HTML内容
            
        Returns:
            List[str]: 图片URL列表
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        img_urls = []
        
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                # 将相对路径转换为绝对URL
                absolute_url = urljoin(url, src)
                img_urls.append(absolute_url)
                
        return img_urls

    def download_image(self, img_url: str, filename: str) -> bool:
        """
        下载并保存图片
        
        Args:
            img_url: 图片URL
            filename: 保存的文件名
            
        Returns:
            bool: 下载成功返回True，否则返回False
        """
        try:
            response = requests.get(img_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # 确定文件保存路径
            file_path = os.path.join(self.save_dir, filename)
            
            # 写入文件
            with open(file_path, 'wb') as f:
                f.write(response.content)
                
            print(f"已保存: {file_path}")
            return True
            
        except requests.RequestException as e:
            print(f"下载失败: {img_url} - {e}")
            return False

    def crawl(self, url: str) -> List[str]:
        """
        执行图片爬取任务
        
        Args:
            url: 目标网页URL
            
        Returns:
            List[str]: 成功下载的图片文件名列表
        """
        # 获取页面内容
        html_content = self.get_page_content(url)
        if not html_content:
            return []
            
        # 提取图片URL
        img_urls = self.extract_image_urls(url, html_content)
        if not img_urls:
            print("未找到图片")
            return []
            
        # 下载所有图片
        downloaded_files = []
        for i, img_url in enumerate(img_urls):
            # 生成文件名
            ext = os.path.splitext(img_url)[1] or '.jpg'
            filename = f"image_{i+1}{ext}"
            
            # 下载图片
            if self.download_image(img_url, filename):
                downloaded_files.append(filename)
                
        return downloaded_files
    # 示例用法
if __name__ == "__main__":
    crawler = ImageCrawler()  # 可指定保存目录 ImageCrawler(save_dir="my_images")
    
    # 预留的URL接口调用
    target_url = "https://haowallpaper.com/"  # 替换为实际目标网址
    downloaded = crawler.crawl(target_url)
    
    print(f"成功下载 {len(downloaded)} 张图片:")
    for filename in downloaded:
        print(f"- {filename}")