# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HaodfItem(scrapy.Item):

    # 杨农
    name = scrapy.Field()
    # yang nong
    pinyin = scrapy.Field()
    # 湖南
    province = scrapy.Field()
    # 长沙
    city = scrapy.Field()
    # 湖南省肿瘤医院肺胃肠肿瘤内科
    hospital = scrapy.Field()
    # 肿瘤内科
    department = scrapy.Field()
    # 主任医师
    title = scrapy.Field()
    # 4.1
    score = scrapy.Field()
    # 肺癌/胃肠肿瘤精准靶向治疗、免疫治疗、疑难复发耐药，肺结节和肺癌早期诊断。最新免疫/靶向治疗药物临床试验
    skill = scrapy.Field()
    # 肺癌
    disease = scrapy.Field()
    # https://yangnong.haodf.com/
    bio_url = scrapy.Field()
    # https://www.haodf.com/jibing/feiai/daifu_xinjiang_all_all_all_all_all_1.htm
    source_url = scrapy.Field()
