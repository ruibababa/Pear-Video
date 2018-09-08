# @Author  : ShiRui

import requests
from lxml import etree
import re
import os


class CrawlLiVideo(object):

	# 必须地址及请求头
	def __init__(self):

		self.index_url = "http://www.pearvideo.com/category_8"
		self.header = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
	}
		self.data = {}

	# 下载网页及解析相应的video地址
	def download(self):

		html = requests.get(self.index_url, self.header).text
		html_etree = etree.HTML(html)
		all_video_urls = html_etree.xpath("//div[@class='vervideo-bd']/a/@href")

		for url in all_video_urls:
			each_video_url = "http://www.pearvideo.com/{}".format(url)
			html_each_url = requests.get(each_video_url, self.header).content.decode("utf-8")
			video_url = re.findall(r'srcUrl="(.*?)"', html_each_url)[0]
			v_name = re.findall(r'<h1 class="video-tt">(.*?)</h1>', html_each_url)[0]
			self.data[v_name] = video_url

		return self.data

	def write_data(self):

		data = self.download()

		if not os.path.exists("video"):
			os.mkdir("video")
		else:
			pass

		for url_keys, url_values in data.items():
			html = requests.get(url_values, self.header)
			with open("video/{}.mp4".format(url_keys), "ab") as f:
				f.write(html.content)
				print("正在下载 %s.mp4, 请稍等。" % url_keys)

if __name__ == '__main__':

	crawl_li_video = CrawlLiVideo()
	crawl_li_video.write_data()
