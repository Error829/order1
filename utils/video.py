import requests
import re


def get_old_view_count(video_url):
    for i in range(5):
        try:
            res = requests.get(
                url=video_url,
                headers={
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                    "referer": "https://m.yangshipin.cn/"
                }
            )
            match_object = re.findall(r'"subtitle":"(.+)次观看","', res.text)
            if not match_object:
                return True, 0
            return True, match_object[0]
        except Exception as e:
            pass
    return False, 0


if __name__ == '__main__':
    # count = get_old_view_count("https://w.yangshipin.cn/video?type=0&vid=y000088hru8")
    count = get_old_view_count("https://w.yangshipin.cn/video?type=0&vid=f0000711h22")
    print(count)
