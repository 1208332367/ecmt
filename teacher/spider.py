import requests

from teacher.models import Teacher, Dept


def get_teachers():
    r=requests.post("https://faculty.ecnu.edu.cn/_wp3services/generalQuery?queryObj=teacherHome",
        data='pageIndex=1&rows=10&conditions=%5B%7B%22field%22%3A%22language%22%2C%22value%22%3A%221%22%2C%22judge%22%3A%22%3D%22%7D%2C%7B%22field%22%3A%22published%22%2C%22value%22%3A%221%22%2C%22judge%22%3A%22%3D%22%7D%5D&orders=%5B%7B%22field%22%3A%22new%22%2C%22type%22%3A%22desc%22%7D%5D&returnInfos=%5B%7B%22field%22%3A%22title%22%2C%22name%22%3A%22title%22%7D%2C%7B%22field%22%3A%22cnUrl%22%2C%22name%22%3A%22cnUrl%22%7D%2C%7B%22field%22%3A%22post%22%2C%22name%22%3A%22post%22%7D%2C%7B%22field%22%3A%22headerPic%22%2C%22name%22%3A%22headerPic%22%7D%2C%7B%22field%22%3A%22department%22%2C%22name%22%3A%22department%22%7D%2C%7B%22field%22%3A%22exField1%22%2C%22name%22%3A%22exField1%22%7D%5D&articleType=1&level=0&pageEvent=doSearchByPage',
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://faculty.ecnu.edu.cn",
            "Referer": "https://faculty.ecnu.edu.cn/_s2/flss/list.psp?keyword=&selectedCareers=&selectedDepartments=8&selectedletters=",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        },
        cookies={
            "Hm_lpvt_9ed81d988505dae403463d657a70a2f3": "1580198367",
            "Hm_lvt_9ed81d988505dae403463d657a70a2f3": "1579683527",
            "JSESSIONID": "01A68E956C54333E984B0F12E8281753",
            "language": ""
        },
    )
    res=r.json()
    r=requests.post("https://faculty.ecnu.edu.cn/_wp3services/generalQuery?queryObj=teacherHome",
        data='pageIndex=1&rows='+ str(res['total']) +'&conditions=%5B%7B%22field%22%3A%22language%22%2C%22value%22%3A%221%22%2C%22judge%22%3A%22%3D%22%7D%2C%7B%22field%22%3A%22published%22%2C%22value%22%3A%221%22%2C%22judge%22%3A%22%3D%22%7D%5D&orders=%5B%7B%22field%22%3A%22new%22%2C%22type%22%3A%22desc%22%7D%5D&returnInfos=%5B%7B%22field%22%3A%22title%22%2C%22name%22%3A%22title%22%7D%2C%7B%22field%22%3A%22cnUrl%22%2C%22name%22%3A%22cnUrl%22%7D%2C%7B%22field%22%3A%22post%22%2C%22name%22%3A%22post%22%7D%2C%7B%22field%22%3A%22headerPic%22%2C%22name%22%3A%22headerPic%22%7D%2C%7B%22field%22%3A%22department%22%2C%22name%22%3A%22department%22%7D%2C%7B%22field%22%3A%22exField1%22%2C%22name%22%3A%22exField1%22%7D%5D&articleType=1&level=0&pageEvent=doSearchByPage',
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://faculty.ecnu.edu.cn",
            "Referer": "https://faculty.ecnu.edu.cn/_s2/flss/list.psp?keyword=&selectedCareers=&selectedDepartments=8&selectedletters=",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        },
        cookies={
            "Hm_lpvt_9ed81d988505dae403463d657a70a2f3": "1580198367",
            "Hm_lvt_9ed81d988505dae403463d657a70a2f3": "1579683527",
            "JSESSIONID": "01A68E956C54333E984B0F12E8281753",
            "language": ""
        },
    )
    res = r.json()
    for t in res['data']:
        _, dept = Dept.objects.get_or_create(name=t['title'])
        _, teacher = Teacher.objects.get_or_create( name='',defaults={
            'name' : t['title'],
            'index_url' : t['cnUrl'],
            'avatar_url' : t['headerPic'],
            'dept' : t['department'],
            'post' : t['post']
        })
    return res

if __name__=="__main__":
    get_teachers()
