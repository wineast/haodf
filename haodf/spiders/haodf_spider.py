# -*- coding: utf-8 -*-
import pypinyin
import scrapy
import copy
import json
from scrapy import Request

from haodf.items import HaodfItem


class HaodfSpiderSpider(scrapy.Spider):
    name = 'haodf_spider'
    allowed_domains = ['haodf.com']
    start_urls = ['https://www.haodf.com/']

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

    #################################爬取上海（某一省份）的所有医院的所有科室的所有医生的信息############################
    def parse(self, response):
        filename = './doctor_cancer.json'
        with open(filename, 'r', encoding='utf-8') as fp:
            diseaseList = json.load(fp)

        for disease in diseaseList:
            item = HaodfItem()
            # item['hospital'] = disease['']
            item['disease'] = disease['type']
            disease_href_root = disease['disease_href']
            totalPage = disease["page"]
            isExtract = disease["enabled"]
            if isExtract:
                for pageNum in range(1,totalPage+1):
                    disease_href = disease_href_root.format(str(pageNum))
                    yield Request(disease_href, meta={'disease': copy.deepcopy(item)}, callback=self.parseDoctorList,
                              dont_filter=True)

    def parseDoctorList(self, response):
        item = response.meta['disease']

        doctorList = response.xpath("//li[@class='hp_doc_box_serviceStar']")
        i = 0
        for doctor in doctorList:
            # bioUrl = doctor.xpath("//div[@class='doctor_photo_serviceStar']/div/p[contains(@class,'doc_head3')]/a/@href")[0].extract()
            # doctorname = doctor.xpath("//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]/p/a/text()")[0].extract()
            # title = doctor.xpath("//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//span[@class='ml15']/text()")[0].extract()
            # hospital = doctor.xpath("//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//span[@class='ml10']/text()")[0].extract()
            # skill =  doctor.xpath("//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//p[contains(text(),'擅长')]/text()")[0].extract()

            bioUrl = doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div/p[contains(@class,'doc_head3')]/a/@href")[0].extract()
            doctorname = doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]/p/a/text()")[0].extract()
            title = doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//span[@class='ml15']/text()")[0].extract()
            hospital = doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//span[@class='ml10']/text()")[0].extract()
            skill =  doctor.xpath(".//div[@class='doctor_photo_serviceStar']/div[contains(@class,'lh180')]//p[contains(text(),'擅长')]/text()")[0].extract()

            item['name'] = self.extractName(doctorname)
            item['pinyin'] = self.pinyinSimple(item['name'])
            item['province'] = ''
            item['city'] = ''
            item['hospital'] = hospital

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
            # i = i + 1

            yield item
        # isPage_num = response.xpath("//div[@class='p_bar']/a[@class='p_text']/text()").extract()
        # if isPage_num:
        #     page_num = re.findall(r"\d+", isPage_num[0])[0]
        #     for p in range(1, int(page_num) + 1):
        #         dephref_sig = dephref[:-4] + "/menzhen_{}.htm".format(p)
        #         yield Request(dephref_sig, meta={'doctor': copy.deepcopy(item)}, callback=self.parseEachDoctorList, dont_filter=True)
        # else:
        #     yield Request(dephref, meta={'doctor': copy.deepcopy(item)}, callback=self.parseEachDoctorList, dont_filter=True)

    def parseEachDoctorList(self, response):
        item = response.meta['doctor']
        doctorlists = response.xpath("//table[@id='doc_list_index']//tr")
        for doctorlist in doctorlists:
            doctorname = doctorlist.xpath("./td[@class='tdnew_a']//a/text()")[0].extract()
            title = doctorlist.xpath("./td[@class='tdnew_a']//p/text()")[0].extract()
            score = doctorlist.xpath("./td[@class='tdnew_b']//i[@class='bigred']/text()")[0].extract()
            item['doctor_name'] = doctorname
            item['doctor_title'] = title
            item['doctor_score'] = score
            yield item
