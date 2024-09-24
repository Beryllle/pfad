import os
import requests
from lxml import etree
import pandas as pd
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # chinese tag
plt.rcParams['axes.unicode_minus'] = False  # regular"-"


excelFileName = "GreekYouTubeMusicVideoTop250.xlsx"
csvFileName = "GreekYouTubeMusicVideoTop250.csv"

headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36'
}

def check() -> bool:

    if os.path.exists(csvFileName) and os.path.exists(excelFileName):
        return True
    else:
        print("file already:", excelFileName, "no repeat")
        return False

def get_first_text(list):
    try:
        return list[0].strip()  # remove blank
    except:
        return ""

def getMovieData():
    df = pd.DataFrame(columns=["Ranking", "ViewCount", "SongTitle", "Artist", "Year"])
    url = "https://ytcharts.com/all-time/"
    res = requests.get(url=url, headers=headers)
    html = etree.HTML(res.text)
    print(res.status_code)
    lis = html.xpath('//*[@id="post-11806"]/div/div/table/tbody/tr')
    print(len(lis))
    for li in lis:
        ranking = get_first_text(li.xpath('./td[1]/text()'))
        count = get_first_text(li.xpath('./td[2]/text()'))
        title = get_first_text(li.xpath('./td[3]/text()'))
        artist = get_first_text(li.xpath('./td[4]/text()'))
        year = get_first_text(li.xpath('./td[5]/text()'))
        print(ranking, count, title, artist, year)
        df.loc[len(df.index)] = [ranking, count, title, artist, year]
    df.to_excel(excelFileName, sheet_name="GreekYouTubeMusicVideoTop250", na_rep="")
    df.to_csv(csvFileName)
    print("file already！")

def datavisualization():
    """
    #visualization
    """
    df = pd.read_csv(filepath_or_buffer=csvFileName)
    
    rating_counts = df['ViewCount'].value_counts().sort_index()
    # pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('GreekMVTop 250ViewCount')
    os.makedirs("images", exist_ok=True)
    plt.savefig('images/GreekMVTop 250ViewCount.png')
    plt.show()

    #histogram
    plt.figure(figsize=(100, 60))
    x = df['Ranking']
    height = df['ViewCount']
    plt.bar(x,height)
    plt.show()



def main():
    if not check():
        getMovieData()
    datavisualization()


if __name__ == '__main__':
    main()


