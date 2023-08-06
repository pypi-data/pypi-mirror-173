from tqdm import *
import requests, os


class EasyPB:
    def __init__(self):
        pass

    def download(self, url=None, filename=None):
        '''
        Download a file from a URL
        :param url:
        :param filename:
        :return:
        '''
        if not filename:
            filename = url.split('/')[-1]
        filename = os.path.join(os.path.abspath('.'),filename)
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        file_size = int(requests.head(url).headers['Content-Length'])
        if os.path.exists(filename):
            first_byte = os.path.getsize(filename)
            print('文件存在，断点续传')
        else:
            first_byte = 0
        header = {'Range': 'bytes=%s-%s' % (first_byte, file_size)}
        pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=url.split('/')[-1],
                    mininterval=0.5)
        result = requests.get(url, headers=header, stream=True)
        with open(filename, 'ab') as f:
            for chunk in result.iter_content(chunk_size=1024):
                f.write(chunk)
                pbar.update(1024)
        pbar.close()
        return file_size


if __name__ == '__main__':
    pb = EasyPB()
    url = 'https://dldir1.qq.com/qqfile/qq/PCQQ9.6.8/QQ9.6.8.28823.exe'
    pb.download(url, 'QQ9.6.8.28823.exe')
