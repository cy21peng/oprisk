# -*- coding: utf-8 -*-

from stanfordcorenlp import StanfordCoreNLP

import pandas as pd
import re
import time

def gettime(result,y):
    y_m = []
    date = []
    behind = ['出生','成立','完成','正式','获准','生','参加','生人','加入','注册','入','入党','由','历任','成立于','创立于','生于','出生于','创立','是','改为','更名','诞生','入职','创建','进入']
    front = ['成立于','创立于','生于','出生于','出生','成立','创立','是','改为','更名','创建于','创建']
    a=1000000 #A arbitrarily large value that is greater than the number of tuples in result guarantees robustness
    for i in range(len(result)):#Iterate over each tuple of result
        if i == a: #if result[a] is to be matched next, it is skipped
            continue
        if result[i][0] in not_date:#If it is a time in the not_date, it is skipped
            continue
        if result[i][1] =='DATE':#If its attribute is DATE, it is placed in the y m list
            if i+1 < len(result)-1 and result[i+1][0] in behind:#If followed by ‘出生’, it is skipped
                continue  
            if i+2 < len(result)-1 and result[i+2][0] in behind:#If followed by ‘出生’, it is skipped
                continue  
            if i+3 < len(result)-1 and result[i+3][0] in behind:#If followed by ‘出生’, it is skipped
                continue
            if i+4 < len(result)-1 and result[i+4][0] in behind:#If followed by ‘出生’, it is skipped
                continue                 
            if i>0 and result[i-1][0] in front:
                continue
            if i>1 and result[i-2][0] in front:
                continue
            y_m = []
            y_m.append(result[i][0]) 
            
            if i+1 > len(result)-1:#If this date is last, there is no need to judge the back. Prevent list index out of range
                continue
            if result[i+1][1] =='DATE':#If its next property is also DATE, it is added at the end of the y_m list. Generally "month"
                y_m.append(result[i+1][0])
                a = i+1 #The next loop, there will be no judgment on the current result[i+1], and continue directly when i==a
                if result[i+1][0] in not_date:
                    del(y_m[-1])
                
                if i+2 > len(result)-1:#If this date is last, there is no need to judge the back. Prevent list index out of range
                    continue
                if result[i+2][1] =='DATE':#If its next attribute is also DATE, it is added at the end of the y_m list, usually "日"
                    y_m.append(result[i+2][0])
                    a = i+2#The next time the loop occurs, the current result[i+2] will not be judged, and continue directly i==a
                    if result[i+2][0] in not_date:
                        del(y_m[-1]) 
            date.append(y_m)

    for d in date:
        if d[0] == '今年':
            d[0] = y
        if d[0] =='去年':
            y2 = y.replace('年','')
    #         print(y2)
            d[0] = str(int(y2)-1)+'年'
        if d[0] =='明年':
            y3 = y.replace('年','')
    #         print(y2)
            d[0] = str(int(y3)+1)+'年'
    return date

def get_yearmin(list_date):
    year = []
#     list_date2 = set(list_date)
    for date2 in list_date :
#         print(date2)
        for date in date2:
            if '年' in date:
#                 print(date)
                year.append(date)
    if year:
#         print(min(year))
        print('all year:',end = '')
        print(year)
        return (min(year))
            
    else:
        return ('none')

def get_yearmax(list_date):
    year = []
#     list_date2 = set(list_date)
    for date2 in list_date :
#         print(date2)
        for date in date2:
            if '年' in date:
#                 print(date)
                year.append(date)
    if year:
#         print(min(year))
        print('all year:',end = '')
        print(year)
        return (max(year))
    else:
        return ('none')

#look for occurence month
def get_monthmin(list_date):
    month = []
    minyear =  get_yearmin(list_date)
#     list_date2 = set(list_date)
    for date2 in list_date :
        for y in range(len(date2)>1):
            if minyear:
                if date2[y] == minyear :
                    if date2[y+1]:
                        month.append(date2[y+1])
    if month:
#         print(min(year))
        print('all months of the occurence year:',end = '')
        print(month)
        return (min(month))
    else:
        return ('none')

#Look for the end of the month
def get_monthmax(list_date):
    month = []
    maxyear =  get_yearmax(list_date)
#     list_date2 = set(list_date)
    for date2 in list_date :
        for y in range(len(date2)>1):
            if maxyear:
                if date2[y] == maxyear :
                    if date2[y+1]:
                        month.append(date2[y+1])
    if month:
#         print(min(year))
        print('All months of the end year:',end = '')
        print(month)
        return (max(month))
    else:
        return ('none')


# identify bank
def getbank(sentence):
    bank = []
    banks = []
    for key,value in bank_dict.items():
    #     print(value)
        for val in value:
    #         print(val)
            if val in sentence:
                bank.append(key)
    bank2 = set(bank)
    banks.append(','.join(bank2))
    
    return banks[0]

# identify names
def getperson(list_person):
    person = []
    list_person2 = set(list_person)
    person.append(','.join(list_person2)) 

    return person[0]


def sort_key(s):
    #sort_strings_with_embedded_numbers
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(s) # Cut into numbers and non-numbers
#    print(pieces)
    pieces[1::2] = map(float, pieces[1::2])  # Converts the part of a number to an integer
    return pieces


#identify loss amount
def getmoney(list_money):
    #All converted to numbers
    money2 = []
    for money in list_money:
        if '几' in money:
            continue
        try:
            if _trans(money):#If it is already a number, _trans returns 0
                money2.append(trans(money))
            else:
                money2.append(money)
        except:
            money = 0
        # print(money2) 

    #Remove '万'and'亿', and convert them into a number
    money3 = []
    for s in money2:
        re_digits = re.compile(r'(\d+)')
        s = str(s)
        pieces = re_digits.split(s) # Cut into numbers and non-numbers
    #     print(pieces)
        pieces[1::2] = map(float, pieces[1::2])# Converts the part of a number to an integer
    #     print(pieces[1::2] )
    #     print(len(pieces[1::2]))
        num = 0
        if pieces[1::2]:
            num = pieces[1::2][0]
            if len(pieces[1::2])>1:#If there are decimals
                if pieces[1::2][1]<10:
                    num = pieces[1::2][0]+ pieces[1::2][1]*0.1
                elif pieces[1::2][1]>9 and pieces[1::2][1]<100:
                    num = pieces[1::2][0]+ pieces[1::2][1]*0.01
                elif pieces[1::2][1]>99 and pieces[1::2][1]<1000:
                    num = pieces[1::2][0]+ pieces[1::2][1]*0.001
                elif pieces[1::2][1]>999 and pieces[1::2][1]<10000:
                    num = pieces[1::2][0]+ pieces[1::2][1]*0.0001
                else:
                    num = pieces[1::2][0]+ pieces[1::2][1]*0.000001
    #         print(num)
            idx_w,idx_y = s.find('万'),s.find('亿')
            if idx_w != -1:
                num = num*10000
            if idx_y != -1:
                num = num*100000000
            money3.append(num)
    #     print(money3)

    # print(money3)
    if money3:
        print('all money:',end = '')
        print(money3)
#        print(max(money3))
        a = max(money3)*0.0001
        return(str(a)+'(10000CNY)')
    else:
        return 'none'

#Chinese numerals to Arabic numerals
digit = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,'两': 2}
def _trans(s):
    num = 0
    if s:
        idx_q, idx_b, idx_s = s.find('千'), s.find('百'), s.find('十')
        if idx_q != -1:
            num += digit[s[idx_q - 1:idx_q]] * 1000
        if idx_b != -1:
            num += digit[s[idx_b - 1:idx_b]] * 100
        if idx_s != -1:
            num += digit.get(s[idx_s - 1:idx_s], 1) * 10
        if s[-1] in digit:
            num += digit[s[-1]]
    return num

def trans(chn):
    chn = chn.replace('零', '')
    idx_y, idx_w = chn.rfind('亿'), chn.rfind('万')
    str1 = '亿'
    str2 = '万'
    if idx_w < idx_y:
        idx_w = -1
    num_y, num_w = 100000000, 10000
    if idx_y != -1 and idx_w != -1:
        return str(trans(chn[:idx_y]) + _trans(chn[idx_y + 1:idx_w])*0.0001)+str1
    elif idx_y != -1:
        return str(trans(chn[:idx_y]))+str1
    elif idx_w != -1:
        return str(_trans(chn[:idx_w]))+str2
    return _trans(chn)

#identify province name
def getprovince(sentence):
    pro_list = []
    for pro in province_dict:
        if pro in sentence:
            print(pro)
            pro_list.append(pro)
    return pro_list

#identify city name
def getcity(sentence):
    city_list = []
    for ci in city_total:
        if ci in sentence:
            print(ci)
            city_list.append(ci)
    return city_list


if __name__ == '__main__': 
    start2 = time.time()
    text_pd = pd.read_excel(r'text_OR_mark.xlsx', index_col=[0])#
    not_date = ['此前','当月','目前','当时','近日','日前','近年','上半年','下半年','半年','最近','昨日','近几年']
    not_person = ['本报讯','查阅到','中邮储','更应该','秋老虎','截稿日','曾用名']
    not_money = ['元','万余','百万余','英镑','美元','法郎','欧元','卢布','加元','百亿','千万','万亿','万','数千万','数百万','数十万','数十亿','数万','百万']
    #Construct bank dictionary
    bank_pd = pd.read_excel(r'bank_dict.xlsx', index_col=[0])
    print('bank dictionary loading finish')
    bank_pd = bank_pd.fillna(0)
    bank_dict= { }
    for  no,bank in bank_pd.iloc[:,0:4].iterrows():
        bank_jian = []
        for i in range(len(bank)):
    #        print(i)
            if bank[i]:
                bank_jian.append(bank[i])
    #        print(bank_jian)
        bank_dict[bank[0]] = bank_jian
        
    #Construct province list
    df_province = pd.read_excel(r"province_dict.xlsx",usecols=['省份'])
    df_province_li = df_province.values.tolist()
    province_dict= []
    for s_li in df_province_li:
        province_dict.append(s_li[0])
    
    #Construct pcity list
    city_pd= pd.read_excel(r'city_dict.xlsx', index_col=[0])
    city_pd = city_pd.fillna(0)
    city_total= []  
    for  no,city in city_pd.iloc[:,:].iterrows():
        for i in range(len(city)):
            if city[i]:
                city[i]=str(city[i]).replace(u'\u3000',u' ')
                city_total.append(city[i])
    
    nlp = StanfordCoreNLP(r'D:\Stanford\Stanford CoreNLP', lang="zh")
    for  no,text in text_pd.iloc[:,0:10].iterrows():
        minyear2 = []
        minmonth2 = []
        maxyear2 = []
        maxmonth2 = []
        person2 = []
        money2 = []
        bank2 = []
        
        start = time.time()
        print(no)
        sentence = text['article']
        y = text['year']
        print("start named entity recognition！")
        result = nlp.ner(sentence)
        print('named entity recognition result:')
        print(result)
        print("finish named entity recognition！")
        datelist = gettime(result,y)
        print("datelist:",end ='')
        print(datelist)
        
        minyear =  get_yearmin(datelist)
        print('-----occurrence year：',end= '')
        print(minyear)
        minyear2.append(minyear)
        text_pd.loc[no,"occurrence year"] = ','.join(minyear2)
        
        minmonth = get_monthmin(datelist)
        print('-----occurrence month：',end= '')
        print(minmonth)
        minmonth2.append(minmonth)
        text_pd.loc[no,"occurrence month"] = ','.join(minmonth2)
        
        maxyear =  get_yearmax(datelist)
        print('-----end year：',end= '')
        print(maxyear)
        maxyear2.append(maxyear)
        text_pd.loc[no,"end year"] = ','.join(maxyear2)
        
        maxmonth = get_monthmax(datelist)
        print('-----end month：',end= '')
        print(maxmonth) 
        maxmonth2.append(maxmonth)
        text_pd.loc[no,"end month"] = ','.join(maxmonth2)
        
        list_person = []
        list_money = []
        for i in result:
            if i[1] == 'PERSON':#person involved
                if i[0] not in not_person:
                    list_person.append(i[0])
            if i[1] == 'MONEY':#loss amount
                if i[0] not in not_money:
                    list_money.append(i[0])

        person = getperson(list_person)
        print('----person involved:',end='')
        print(person)
        person2.append(person)
        text_pd.loc[no,"person involved"] = ','.join(person2)
        
        money = getmoney(list_money)
        print('----loss amount:',end='')
        print(money)
        money2.append(money)
        text_pd.loc[no,"loss amount"] = ','.join(money2)
        
        bank = getbank(sentence)
        print('----bank involved:',end='')
        print(bank)
        bank2.append(bank)
        text_pd.loc[no,"bank involved"] = ','.join(bank2)
        
        province = getprovince(sentence)
        print('----province occurred:',end='')
        print(province)
        text_pd.loc[no,"province occurred"] = ','.join(province)
        
        city = getcity(sentence)
        print('----city occurred:',end='')
        print(city)
        text_pd.loc[no,"city occurred"] = ','.join(city)
        
        end = time.time()
        print('runtime：',end ='')
        print(end-start)
    nlp.close()
    end2 = time.time()
    print('total runtime(sec):',end = ' ')
    print(end2-start2)

text_pd.to_excel(r'result-NER.xlsx')
#If you process too many items at once, you may exceed the storage limit of to_excel, and you can save them in CSV form first