import feedparser
import subprocess
import os
import time

# ssh-agent 실행
ssh_agent = subprocess.Popen(['ssh-agent', '-s'], stdout=subprocess.PIPE)
# ssh-add 실행
subprocess.call('ssh-add ~/.ssh/id_rsa', shell=True)
# RSS 피드 URL 설정

rss_url = "http://www.yonhapnewstv.co.kr/browse/feed/"
# feedparser로 RSS 뉴스 기사 파싱
feed = feedparser.parse(rss_url)

# 저장할 파일 경로와 파일명 설정
base_path = "/home/dls32208/Documents/VRChatKoreaNews"
file_name = "news.html"


rss_urls = {
    '조선일보': {
        '전체기사': 'https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml',
        '정치': 'https://www.chosun.com/arc/outboundfeeds/rss/category/politics/?outputType=xml',
        '경제': 'https://www.chosun.com/arc/outboundfeeds/rss/category/economy/?outputType=xml',
        '사회': 'https://www.chosun.com/arc/outboundfeeds/rss/category/national/?outputType=xml',
        '국제': 'https://www.chosun.com/arc/outboundfeeds/rss/category/international/?outputType=xml',
        '문화라이프': 'https://www.chosun.com/arc/outboundfeeds/rss/category/culture-life/?outputType=xml',
        '오피니언': 'https://www.chosun.com/arc/outboundfeeds/rss/category/opinion/?outputType=xml',
        '스포츠': 'https://www.chosun.com/arc/outboundfeeds/rss/category/sports/?outputType=xml',
        '연예': 'https://www.chosun.com/arc/outboundfeeds/rss/category/entertainments/?outputType=xml'
    },
    '동아일보': {
        '전체기사': 'https://rss.donga.com/total.xml',
        '정치': 'https://rss.donga.com/politics.xml',
        '사회': 'https://rss.donga.com/national.xml',
        '경제': 'https://rss.donga.com/economy.xml',
        '국제': 'https://rss.donga.com/international.xml',
        '사설칼럼': 'https://rss.donga.com/editorials.xml',
        '의학과학': 'https://rss.donga.com/science.xml',
        '문화연예': 'https://rss.donga.com/culture.xml',
        '스포츠': 'https://rss.donga.com/sports.xml',
        '사람속으로': 'https://rss.donga.com/inmul.xml',
        '건강': 'https://rss.donga.com/health.xml',
        '레져': 'https://rss.donga.com/leisure.xml',
        '도서': 'https://rss.donga.com/book.xml',
        '공연': 'https://rss.donga.com/show.xml',
        '여성': 'https://rss.donga.com/woman.xml',
        '여행': 'https://rss.donga.com/travel.xml',
        '생활정보': 'https://rss.donga.com/lifeinfo.xml',
        '스포츠': 'https://rss.donga.com/sportsdonga/sports.xml',
        '야구MLB': 'https://rss.donga.com/sportsdonga/baseball.xml',
        '축구': 'https://rss.donga.com/sportsdonga/soccer.xml',
        '골프': 'https://rss.donga.com/sportsdonga/golf.xml',
        '일반': 'https://rss.donga.com/sportsdonga/sports_general.xml',
        'e스포츠': 'https://rss.donga.com/sportsdonga/sports_game.xml',
        '엔터테인먼트': 'https://rss.donga.com/sportsdonga/entertainment.xml',
    },
    '매일경제': {
        '헤드라인': 'https://www.mk.co.kr/rss/30000001/',
        '전체뉴스': 'https://www.mk.co.kr/rss/40300001/',
        '경제': 'https://www.mk.co.kr/rss/30100041/',
        '정치': 'https://www.mk.co.kr/rss/30200030/',
        '사회': 'https://www.mk.co.kr/rss/50400012/',
        '국제': 'https://www.mk.co.kr/rss/30300018/',
        '기업경영': 'https://www.mk.co.kr/rss/50100032/',
        '증권': 'https://www.mk.co.kr/rss/50200011/',
        '부동산': 'https://www.mk.co.kr/rss/50300009/',
        '문화연예': 'https://www.mk.co.kr/rss/30000023/',
        '스포츠': 'https://www.mk.co.kr/rss/71000001/',
        '게임': 'https://www.mk.co.kr/rss/50700001/',
        'MBA': 'https://www.mk.co.kr/rss/40200124/',
        '머니앤리치스': 'https://www.mk.co.kr/rss/40200003/',
        'English': 'https://www.mk.co.kr/rss/30800011/',
        '이코노미': 'https://www.mk.co.kr/rss/50000001/',
        '시티라이프': 'https://www.mk.co.kr/rss/60000007/'
    }
}


for press in rss_urls:
    file_name = f"{press}.html"
    file_path = os.path.join(base_path, file_name)
    press_html = ""
    for category in rss_urls[press]:
        rss_url = rss_urls[press][category]
        # feedparser로 RSS 뉴스 기사 파싱
        feed = feedparser.parse(rss_url)
        print(rss_url)
        # 기사 정보를 HTML 코드로 변환하여 press_html에 추가
        press_html += f"<h1>{category}</h1>\n"
        for entry in feed.entries:
            press_html += f"<h2><a href='{entry.link}'>{entry.title}</a></h2>\n"
            if(entry.summary>entry.description):
                press_html += f"<p>{entry.summary}</p>\n\n"
            else:
                press_html += f"<p>{entry.description}</p>\n\n"
    # HTML 파일 생성
    with open(file_path, "w") as f:
        f.write("<html>\n<head>\n<title>News</title>\n</head>\n<body>\n")
        f.write(press_html)
        f.write("</body>\n</html>")

    # 각 언론사별로 commit 및 push
    press_path = os.path.join(base_path, press)
    subprocess.call(f"git add {file_path}", cwd=press_path, shell=True)
    subprocess.call(f"git commit -m 'Update news' && git push", cwd=press_path, shell=True)



# ssh-agent 종료
ssh_agent.kill()


"""
# 3분마다 반복 실행
while True:
    # ssh-agent 실행
    ssh_agent = subprocess.Popen(['ssh-agent', '-s'], stdout=subprocess.PIPE)
    # ssh-add 실행
    subprocess.call('ssh-add ~/.ssh/id_rsa', shell=True)

    # feedparser로 RSS 뉴스 기사 파싱
    feed = feedparser.parse(rss_url)

    # html 파일 생성
    with open(os.path.join(base_path, file_name), "w") as f:
        f.write("<html>\n<head>\n<title>News</title>\n</head>\n<body>\n")
        # 뉴스 기사 쓰기
        for entry in feed.entries:
            f.write(f"<h2><a href='{entry.link}'>{entry.title}</a></h2>\n")
            f.write(f"<p>{entry.summary}</p>\n\n")
        f.write("</body>\n</html>")

    # 깃허브에 업로드
    subprocess.call(
        f"cd {base_path} && git add {file_name} && git commit -m 'Update news' && git push", shell=True)

    # ssh-agent 종료
    ssh_agent.kill()
    time.sleep(180)
"""

