import threading
import requests

class DownLoader:
    def download(self, url, callback_word_count):
        print(f'线程：{threading.get_ident()} 开始下载')
        response = requests.get(url)
        response.encoding = 'utf-8'
        callback_word_count(url, response.text) # 调用函数
    
    def start_download(self, url, callback_word_count):
        # self.download(url, callback_word_count) # 阻塞
        thread = threading.Thread(target=self.download,args=(url, callback_word_count)) # 创建线程
        thread.start()

def word_count(url, result):
    print(f"{url}:{len(result)}->{result[:5]}")


def main():
    download = DownLoader()
    download.start_download('http://localhost:8000/novel1.txt',word_count)
    download.start_download('http://localhost:8000/novel2.txt',word_count)
    download.start_download('http://localhost:8000/novel3.txt',word_count)

