# coding = utf-8
"""
@author: zhou
@time:2019/12/12 19:55
@File: views.py
"""

from . import api
from ..models import ZhihuMetrics, ZhihuDetails, ZhihuContent
from datetime import datetime
from ..db_opera import db_opera
from flask import jsonify, request
import requests
import json
from ..tools import token, redis_connection, cut
import time


rd = redis_connection.redis_conn_pool()


def zhihudata():
    current_time = time.strftime('%Y-%m-%d 00:00:00', time.localtime())
    update_time = rd.get('new_update_time') or current_time
    zhihumetrics_data = ZhihuMetrics.query.filter(ZhihuMetrics.update_time > update_time).all()
    metrics_list = db_opera.db_to_list(zhihumetrics_data)
    details_list = []
    for d in metrics_list:
        zhihudetails_data = ZhihuDetails.query.filter_by(hot_cardid=d[1]).first()
        if zhihudetails_data:
            details_list.append([zhihudetails_data.hot_name, zhihudetails_data.hot_link, d[0], d[1], d[2]])

    return details_list


def zhihudetail(hot_id):
    zhihumetrics_details = ZhihuMetrics.query.filter_by(hot_cardid=hot_id).order_by(ZhihuMetrics.update_time).all()
    Column = {'categories': [], 'series': [{'name': '热度走势', 'data': []}]}

    for i in zhihumetrics_details:
        Column['categories'].append(datetime.strftime(i.update_time, "%Y-%m-%d %H:%M"))
        Column['series'][0]['data'].append(int(i.hot_metrics.split()[0]))

    return Column


def zhihucontent(hot_id):
    answer_id = hot_id.split('_')[1]
    zhihu_content = ZhihuContent.query.filter_by(answer_id=answer_id).all()
    content_list = []
    content = ''
    for i in zhihu_content:
        content = content + i.content
        content_list.append(i.content)
    count_word = cut.cut_word(content)

    return count_word, content_list


@api.route('/api/zhihu/hot/', methods=['GET', 'POST'])
@token.tokenRequired
def zhihu_api_data():
    zhihu_data = zhihudata()
    data_list = []
    for data in zhihu_data:
        data_dict = {'title': data[0], 'link': data[1], 'metrics': data[2], 'hot_id': data[3], 'update_time': data[4]}
        data_list.append(data_dict)

    return jsonify({'code': 0, 'content': data_list}), 200


@api.route('/api/zhihu/detail/<id>/', methods=['GET', 'POST'])
@token.tokenRequired
def zhihu_api_detail(id):
    zhihu_detail = zhihudetail(id)
    redis_word = rd.get('wordcloud_%s' %id)
    redis_content = rd.get('content_%s' % id)
    if redis_word:
        count_list = json.loads(redis_word)
        content_list = json.loads(redis_content)
    else:
        count_list = []
        count_word, content_list = zhihucontent(id)  # 获取回答的词频数据和回答内容
        for count in count_word:
            count_list.append({'name': count[0], 'textSize': count[1]})
        rd.set('wordcloud_%s' %id, json.dumps(count_list), ex=604800)
        rd.set('content_%s' %id, json.dumps(content_list), ex=604800)

    if count_list[0]['textSize'] < 10:
        for i in count_list:
            i['textSize'] = i['textSize']*10
    elif count_list[0]['textSize'] > 200:
        for i in count_list:
            i['textSize'] = i['textSize']/10

    return jsonify({'code': 0, 'data': zhihu_detail, 'count_word': count_list, 'content': content_list}), 200


test_content = '''<p>编者按：本文来自<a href=\"https://new.qq.com/omn/TEC20191/TEC2019121300149000.html\" target=\"_blank\">腾讯科技</a>，审校 金鹿，原文标题为：“FTC拟对FB实施禁令，以阻止其旗下产品打通垄断市场”，36氪经授权发布。</p><p>Facebook在今年1月份表示，该公司正在考虑加强其主要平台之间的信息互通功能。但该公司表示，其最近增强互操作性的计划旨在改善用户体验，尤其是考虑到最近Facebook上围绕隐私的争议，而不是为了排挤竞争对手或避开监管行动。</p><p><img alt=\"监管机构拟对Facebook实施禁令，以阻止其旗下产品打通垄断市场\" src=\"https://img.36krcdn.com/20191213/v2_36cd624b9e5e41de92801763f2a88a2f_img_000\" data-img-size-val=\"720,360\"/></p><p>12月13日消息，据外媒报道，据知情人士透露，美国监管机构联邦贸易委员会(FTC)正考虑对Facebook实施初步禁令，旨在阻止Facebook寻求对其产品和技术进行整合，以允许用户使用它们进行跨平台互动，因为此举存在反垄断担忧。</p><p>这些知情人士表示，如果FTC的禁令发布，该机构将主要聚焦于Facebook的政策，涉及如何整合其应用程序或允许它们与潜在竞争对手合作。除了其核心社交网络，Facebook的主要产品还包括Instagram、Messenger和WhatsApp。</p><p>知情人士说，FTC可能采取的行动或会试图阻止Facebook执行这些政策，理由是这些政策存在反垄断之嫌。FTC禁令可能会试图禁止Facebook进一步整合应用程序，联邦监管机构可能会考虑解除这种整合，以作为该公司未来可能拆分的一部分。</p><p>FTC五名成员中大多数人支持寻求实施禁令，而该委员会需要向联邦法院提起诉讼才能获得禁令。FTC和Facebook都拒绝置评。</p><p>知情人士称，这家社交媒体巨头几个月来一直担心FTC会寻求禁止其所谓的“互操作性”规则。互操作性是指数字平台之间交互的方式。这些人士说，担心Facebook的互操作性政策会抑制其他服务的竞争能力，这可能是FTC采取行动的基础。Facebook已经拒绝了对其做法的反复抱怨。</p><p>其中一位知情人士说，监管机构的官员们还担心，Facebook进一步整合自己主要产品的某些计划，可能会让该公司最终在反垄断案中更难被分拆。</p><p>目前尚不清楚FTC是否会对Facebook采取反垄断行动，还是会就其互操作性政策寻求禁令。据知情人士透露，如果该机构采取任何一项措施，最快可能在下个月行动。FTC也有可能试图阻止某些Facebook互操作性政策，批评人士称这些政策在过去曾使竞争对手处于不利地位。</p><p>Facebook在今年1月份表示，该公司正在考虑加强其主要平台之间的信息互通功能。但该公司表示，其最近增强互操作性的计划旨在改善用户体验，尤其是考虑到最近Facebook上围绕隐私的争议，而不是为了排挤竞争对手或避开监管行动。</p><p>Facebook首席执行官说马克 扎克伯格今年3月在Facebook上的一篇帖子中写道：“互操作性具有隐私和安全方面的优势，通过我们的各种服务发送信息，你将能够从Messenger向WhatsApp中某人的电话号码发送加密信息。”</p><p>美国司法部正在对美国最大科技公司涉嫌垄断行为进行调查。大约20年前，一起类似的案件曾威胁到微软的命运。即时通讯网络越来越受欢迎，尤其是在年轻用户中，而且对Facebook的业务越来越重要。该公司希望更新其平台以应对这一趋势。</p><p>美国哥伦比亚大学法学教授蒂姆·吴（Tim Wu）曾是FTC的前高级顾问，他表示，寻求初步禁令可能会为FTC带来战略优势。他解释称：“这样做的好处是让事情有了进展，而且可以很快地迫使进行司法裁决，而不是让反垄断调查持续五年时间。对政府来说，举证的负担可能更重，但如果他们有很好的判例，这可能是有利的。”</p><p>蒂姆·吴是Facebook的批评者之一，他们认为该公司追求更紧密的整合是在隐藏反竞争动机。这些人已经向FTC提议，应该申请一项禁令，阻止该公司进一步的互操作性计划。</p><p>今年夏天，Facebook的批评者向反垄断监管机构提交了一份文件，里面称：“整合的一个预期影响是使拆分变得更加困难，初步禁令可能是必要的或可取的，以防止这种合并，并维持现状。”这份文件的提交者包括蒂姆·吴和纽约大学法学教授斯科特·亨菲尔（Scott Hemphill）。</p><p>迅速转向互操作性的诉讼也可以让FTC在美国司法部之前采取执法行动。这两个机构共享联邦反垄断执法机构的权力，偶尔也会成为竞争对手。</p><p>据悉，这两家机构都在调查Facebook可能涉及的反垄断问题。FTC对Facebook提起的反垄断诉讼，可能成为联邦执法者对大型科技公司采取行动的先兆，因为这些机构也在调查谷歌以及亚马逊的类似问题，多州总检察长也在调查Facebook和谷歌。</p><p>今年8月份的报道显示，FTC一直在审查Facebook的收购交易，将其作为反垄断调查的核心内容之一，以确定这些交易是否属于旨在消灭潜在竞争对手、防范竞争威胁的行动。根据标普全球(S&amp;P Global)汇编的数据，过去15年里，Facebook收购了大约90家公司，包括Instagram和WhatsApp。</p><p>在今年早些时候的国会听证会上，Facebook前公共政策主管马特·佩劳特（Matt Perault）告诉众议院反垄断小组委员会，该公司的收购促进了创新，并将被Facebook收购的公司以优势互补的方式整合起来。作为Facebook的一部分，它们有更多的机会进行创新，从而提升用户体验，为更多人带来更丰富的选择。</p>
'''


@api.route('/api/zhihu/url/')
def zhihu_url():
    headers = {"User-Agent": "", "Cookie": ""}
    url = 'https://www.zhihu.com/question/360570348'
    res = requests.get(url, headers=headers)
    content = res.content.decode()
    # print(content)
    # print(type(content))
    zhihucontent('Q_68262075')
    return jsonify({'code': 0, 'content': test_content}), 200
