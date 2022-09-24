from urllib import urlopen

import bs4


def grab(pages):
    """

    :param pages: list of youporn catalogue pages
    """
    video_page_urls = []
    for catalog_page in pages:
        html = urlopen(catalog_page).read().decode()
        bs = bs4.BeautifulSoup(html)
        video_page_urls.extend(bs.find("div", "videoList").find_all("a"))
    video_page_urls = [("http://www.youporn.com" + a['href']) for a in video_page_urls]

    for n, catalog_page in enumerate(video_page_urls):
        html = urlopen(catalog_page).read().decode()
        bs = bs4.BeautifulSoup(html)
        download_link = bs.find_all("div", "downloadOption")[0].find("a")['href']
        title = bs.title.text.replace(" - Free Porn Videos - YouPorn", "")
        print(n, "Loading", title)
        data = urlopen(download_link).read()
        with open("/Users/gan/ffmpeg/" + title + ".mp4", mode="bw") as file:
            print("... writing")
            file.write(data)
        print("... DONE!")


if __name__ == "__main__":

    catalogue_pages = ["http://www.youporn.com/uservids/foldvideo/?page=1"]

    if len(catalogue_pages) == 0:
        print("""Please provide catalogue_pages links to download. Example:
    catalogue_pages = [
        "http://www.youporn.com/uservids/foldvideo/?page=1",
        "http://www.youporn.com/uservids/foldvideo/?page=2",
        "http://www.youporn.com/uservids/foldvideo/?page=3"
    ]""")
    else:
        grab(catalogue_pages)
