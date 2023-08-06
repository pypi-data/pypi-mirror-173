import platform
import requests
from tqdm import tqdm


def get_sys_info():
    platform_info = platform.uname()
    return platform_info


def download(url, name):
    res = requests.get(url, stream=True)
    total_length = res.headers.get('content-length')

    if total_length is None:
        with open(name, 'wb') as f:
            f.write(res.content)
            f.close()
        return 0

    total_length = int(total_length)
    with open(name, 'wb') as file:
        for data in tqdm(iterable=res.iter_content(), total=total_length, unit='KB', desc=name):
            file.write(data)
        file.close()
