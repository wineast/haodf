# -*- coding: utf-8 -*-
import logging

import pypinyin
import scrapy
import copy
import json
from scrapy import Request

from haodf.items import HaodfItem

logger = logging.getLogger("haodfLogger")

class HaodfSpiderSpider(scrapy.Spider):
    name = 'haodf_spider'
    allowed_domains = ['haodf.com']
    start_urls = ['https://www.haodf.com/']
    # 少最后一个page参数, page直接append上去
    PAGE_URL_FORMATTER = 'https://www.haodf.com/jibing/{}/daifu_{}_{}_{}_{}_{}_{}_'
    HDF_REGION_LIST = [
        # ['北京', 'beijing'],
        ['天津', 'tianjin']
        # ,
        # ['河北', 'hebei'],
        # ['山西', 'sx'],
        # ['内蒙古', 'neimenggu'],
        # ['辽宁', 'liaoning'],
        # ['吉林', 'jilin'],
        # ['黑龙江', 'heilongjiang'],
        # ['上海', 'shanghai'],
        # ['江苏', 'jiangsu'],
        # ['浙江', 'zhejiang'],
        # ['安徽', 'anhui'],
        # ['福建', 'fujian'],
        # ['江西', 'jiangxi'],
        # ['山东', 'shandong'],
        # ['河南', 'henan'],
        # ['湖北', 'hubei'],
        # ['湖南', 'hunan'],
        # ['广东', 'guangdong'],
        # ['广西', 'guangxi'],
        # ['海南', 'hainan'],
        # ['重庆', 'chongqing'],
        # ['四川', 'sichuan'],
        # ['贵州', 'guizhou'],
        # ['云南', 'neimenggu'],
        # ['西藏', 'xizang'],
        # ['陕西', 'shanxi'],
        # ['甘肃', 'gansu'],
        # ['青海', 'qinghai'],
        # ['宁夏', 'ningxia'],
        # ['新疆', 'xinjiang']
    ]

    def pinyinSimple(self, word):
        s = ''
        for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
            s += ''.join(i)
        return s
    # 删除名字里的空格和点号
    def extractName(self, name):
        newName = name.replace(' ', '').replace('.', '')
        return newName
    # def parse(self, response):
    #     url = "https://www.haodf.com/yiyuan/shanghai/list.htm"
    #     yield Request(url, callback=self.parseMainPage)

    #########################爬取全国各省市的医院################################
    # def parseProvince(self, response):
    #     provinces = response.xpath("//div[@id='el_tree_1000000']//div")
    #     for province in provinces:
    #         pro = province.xpath("./a/text()").extract()
    #         if pro:
    #             item = HaodfItem()
    #             item['province'] = pro[0]
    #             href = province.xpath("./a/@href")[0].extract()
    #             province_href = "https:" + href
    #             yield Request(province_href, meta={'province': copy.deepcopy(item)}, callback=self.parseMainPage, dont_filter=True)

    # def parseMainPage(self, response):
    #     item = response.meta['province']
    #     hosp_divs = response.xpath("//div[@class='m_ctt_green']")
    #     city_divs = response.xpath("//div[@class='m_title_green']/text()").extract()
    #     i = 0
    #     for district_hosp in hosp_divs:
    #         city_name = city_divs[i]
    #         # if "其他地区" not in city_name:
    #
    #         #     city_name = city_name + "区"
    #         i = i + 1
    #         name = district_hosp.xpath("./ul/li/a/text()").extract()
    #         href = district_hosp.xpath("./ul/li/a/@href").extract()
    #
    #         for x in range(0, len(name)):
    #             item['city'] = city_name
    #             item['hospital'] = name[x]
    #             item['hospital_href'] = "http://www.haodf.com" + href[x]
    #             hosp_url = "https://www.haodf.com" + href[x]
    #             yield Request(hosp_url, meta={'hospital': copy.deepcopy(item)}, callback=self.parseDepartment, dont_filter=True)
    #
    # def parseDepartment(self, response):
    #     item = response.meta['hospital']
    #     hospitalTitle = response.xpath("//div[@class='h-d-title']")
    #     if hospitalTitle:
    #         hospTitle = hospitalTitle[0]
    #         # name = hospTitle.xpath("./h1/text()")[0]
    #         otherinfo = len(hospTitle.xpath("./span/text()"))
    #         if(otherinfo == 2):
    #             level = hospTitle.xpath("./span/text()")[0].extract()
    #             hosptype = hospTitle.xpath("./span/text()")[1].extract()
    #         elif(otherinfo == 1):
    #             level = ""
    #             hosptype = hospTitle.xpath("./span/text()")[0].extract()
    #         else:
    #             level = ""
    #             hosptype = ""
    #         telephone = response.xpath("//p[@class='h-d-c-item js-phone-wrap']/span/text()")[1].extract()
    #         item['hospital_level'] = level
    #         item['hospital_type'] = hosptype
    #         item['telephone'] = telephone
    #
    #     departmentList = response.xpath("//div[@class='m-hospital']")[0]
    #     num = departmentList.xpath("./div[@class='m-h-title']/span/text()")[0].extract()
    #     depNum = re.findall(r"\d+",num)[0]
    #     docTotalNum = re.findall(r"\d+",num)[1]
    #     item['department_num'] = depNum
    #     item['doctorTotal_num'] = docTotalNum
    #
    #     yield item

    #################################爬取上海（某一省份）的所有医院的所有科室信息############################
    # def parseMainPage(self, response):
    #     hosp_divs = response.xpath("//div[@class='m_ctt_green']")
    #     city_divs = response.xpath("//div[@class='m_title_green']/text()").extract()
    #     i = 0
    #     for district_hosp in hosp_divs:
    #         city_name = city_divs[i]
    #         # if "其他地区" not in city_name:
    #         #     city_name = city_name + "区"
    #         i = i + 1
    #         name = district_hosp.xpath("./ul/li/a/text()").extract()
    #         href = district_hosp.xpath("./ul/li/a/@href").extract()
    #
    #         for x in range(0, len(name)):
    #             item = HaodfItem()
    #             # item['province'] = '上海'
    #             # item['city'] = city_name
    #             item['hospital'] = name[x]
    #             # item['hospital_href'] = "http://www.haodf.com" + href[x]
    #             hosp_url = "https://www.haodf.com" + href[x]
    #             yield Request(hosp_url, meta={'hospital': copy.deepcopy(item)}, callback=self.parseDepartment, dont_filter=True)
    #
    # def parseDepartment(self, response):
    #     item = response.meta['hospital']
    #     # hospitalTitle = response.xpath("//div[@class='h-d-title']")
    #     # if hospitalTitle:
    #     #     hospTitle = hospitalTitle[0]
    #     #     # name = hospTitle.xpath("./h1/text()")[0]
    #     #     otherinfo = len(hospTitle.xpath("./span/text()"))
    #     #     if (otherinfo == 2):
    #     #         level = hospTitle.xpath("./span/text()")[0].extract()
    #     #         hosptype = hospTitle.xpath("./span/text()")[1].extract()
    #     #     elif (otherinfo == 1):
    #     #         level = ""
    #     #         hosptype = hospTitle.xpath("./span/text()")[0].extract()
    #     #     else:
    #     #         level = ""
    #     #         hosptype = ""
    #     #     telephone = response.xpath("//p[@class='h-d-c-item js-phone-wrap']/span/text()")[1].extract()
    #     #     item['hospital_level'] = level
    #     #     item['hospital_type'] = hosptype
    #     #     item['telephone'] = telephone
    #
    #     departmentList = response.xpath("//div[@class='m-hospital']")[0]
    #     # num = departmentList.xpath("./div[@class='m-h-title']/span/text()")[0].extract()
    #     # depNum = re.findall(r"\d+", num)[0]
    #     # docTotalNum = re.findall(r"\d+", num)[1]
    #     # item['department_num'] = depNum
    #     # item['doctorTotal_num'] = docTotalNum
    #
    #
    #     deps = departmentList.xpath("./ul[@class='faculty-list']")[0]
    #
    #     depnames = deps.xpath("//div[@class='f-l-i-s-i-wrap']/a/text()").extract()
    #     dephrefs = deps.xpath("//div[@class='f-l-i-s-i-wrap']/a/@href").extract()
    #     depDocNums = []
    #     num = deps.xpath(".//div[@class='f-l-i-s-i-wrap']/p/text()").extract()
    #     for n in num:
    #         deparTotalNum = re.findall(r"\d+", n)
    #         if deparTotalNum:
    #             depDocNums.append(deparTotalNum[0])
    #
    #     for x in range(0, len(depnames)):
    #         item['department'] = depnames[x]
    #         item['department_href'] = "https:"+dephrefs[x]
    #         item['doctorDep_num'] = depDocNums[x]
    #         # department_url = "https:"+dephrefs[x]
    #         yield item
    #         # yield Request(department_url, meta={'department': copy.deepcopy(item)}, callback=self.parseDoctorList, dont_filter=True)



    def start_requests(self):
        # 拼装链接
        # region_list = self.settings.getlist['REGION_LIST']
        region_list = self.HDF_REGION_LIST
        url_format = self.settings['URL_FORMATTER']

        filename = './doctor_cancer_prod.json'
        with open(filename, 'r', encoding='utf-8') as fp:
            diseaseList = json.load(fp)
        diseaseSet = set('')

        for disease in diseaseList:

            isExtract = disease.get('enabled',True)
            if not isExtract:
                logger.warning("{} not enabled to crawler".format(diseaseType))
                continue

            # fix me here,如果type没有值怎么办
            diseaseType = disease.get('type','')
            if len(diseaseType) == 0:
                logger.warning("no disease type is found, just continue")
                continue

            # 检查是否在已经取过了
            if diseaseType in diseaseSet:
                logger.warning("{} is in the crawler list".format(diseaseType))
                continue
            else:
                diseaseSet.add(diseaseType)
            # 默认情况下，链接地址由 病名的拼音构成，有些情况需要人为介入
            diseaseTypePinyinRaw = disease.get('type_pinyin', '')
            if len(diseaseTypePinyinRaw) == 0:
                diseaseTypePinyin = self.pinyinSimple(diseaseType)
            else:
                diseaseTypePinyin = diseaseTypePinyinRaw

            pageEnd = disease.get('page_end',100)

            # 根据地区组装爬虫链接
            for region in region_list:
                urlToCrawler = url_format.format(diseaseTypePinyin,region[1],'all','all','all','all','all','1')
                pageUrlToCrawler = self.PAGE_URL_FORMATTER.format(diseaseTypePinyin,region[1],'all','all','all','all','all')
                logger.info('start crawler: ' + urlToCrawler)
                # yield Request(url[0], self.parse)
                # yield Request(disease_href, meta={'disease': copy.deepcopy(item)}, callback=self.parseDoctorList, dont_filter=True)
                yield Request(urlToCrawler, meta={'region': region[0],'diseaseType':diseaseType,'pageEnd':pageEnd,'pageUrlToCrawler':pageUrlToCrawler}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        region = response.meta['region']
        diseaseType = response.meta['diseaseType']
        pageEnd = response.meta['pageEnd']
        pageUrlToCrawler = response.meta['pageUrlToCrawler']

        # 查找start-end 页面
        totalPageList = response.xpath("//div[@class='page_turn']/a[@class='page_turn_a']/span/font/text()")
        # 有且仅有一页
        doctornameList = response.xpath(".//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]/p/a/text()")

        if len(totalPageList) == 0:
            if len(doctornameList) == 0:
                logger.warning("no page found for this {},{},{}".format(region,diseaseType,pageUrlToCrawler))
                return
            else:
                totalPage = 1
        else:
            totalPage = totalPageList[0].extract()

        for pageNum in range(1,int(totalPage)+1):
            pageUrl = pageUrlToCrawler + str(pageNum) + '.htm'
            logger.info('page url is: ' + pageUrl)
            yield Request(pageUrl, meta={'region': region,'diseaseType':diseaseType,'pageEnd':pageEnd,'pageUrl':pageUrl}, callback=self.parseDoctorList, dont_filter=True)

    def parseDoctorList(self, response):
        item = HaodfItem()
        region = response.meta['region']
        diseaseType = response.meta['diseaseType']
        pageUrl = response.meta['pageUrl']

        doctorList = response.xpath("//li[@class='hp_doc_box_serviceStar']")
        for doctor in doctorList:
            # bioUrl = doctor.xpath("//div[@class='doctor_photo_serviceStar']/div/p[contains(@class,'doc_head3')]/a/@href")[0].extract()
            # doctorname = doctor.xpath("//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]/p/a/text()")[0].extract()
            # title = doctor.xpath("//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//span[@class='ml15']/text()")[0].extract()
            # hospital = doctor.xpath("//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//span[@class='ml10']/text()")[0].extract()
            # skill =  doctor.xpath("//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//p[contains(text(),'擅长')]/text()")[0].extract()

            bioUrl = doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div/p[contains(@class,'doc_head3')]/a/@href")[0].extract()
            doctorname = doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]/p/a/text()")[0].extract()
            titleList = doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//span[@class='ml15']/text()")
            if len(titleList) == 0:
                title = ''
            else:
                title = titleList[0].extract()

            hospital = doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//span[@class='ml10']/text()")[0].extract()
            skill = doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//p[contains(text(),'擅长')]/text()")[0].extract()
            scoreList = doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//span[@class='patient_recommend']/a/i/text()")
            if len(scoreList) == 0:
                score = ''
            else:
                score = scoreList[0].extract()
            # http://www.360doc.com/content/09/1211/21/178233_10904192.shtml
            item['name'] = self.extractName(doctorname)
            item['pinyin'] = self.pinyinSimple(item['name'])
            item['province'] = region
            item['city'] = ''
            item['hospital'] = hospital
            item['score'] = score

            # select distinct hospital from doctor_raw where department = '' and hospital not like '%中心%' and hospital not like '%工作室%' and hospital not like '%门诊部%'
            dList = hospital.split('院')
            if len(dList) > 1:
                if dList[-1].startswith(')'):
                    item['department'] = dList[-1][1:]
                else:
                    item['department'] = dList[-1]
            else:
                item['department'] = ''

            item['title'] = title
            item['skill'] = skill.strip()
            item['bio_url'] = bioUrl
            item['source_url'] = pageUrl
            item['disease'] = diseaseType

            yield item