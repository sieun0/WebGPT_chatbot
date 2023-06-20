var cheerio = require('cheerio');
var request = require('request'); //원하는 페이지에 request 요청을 보내기 위해
var https = require("https");
var fs = require('fs');
//const EventEmitter = require('events');
require('events').EventEmitter.defaultMaxListeners = 20;
//const readline = require("readline");
var list =[];
const data = process.argv[2];
var encodedData = encodeURIComponent(data);

//const emitter = new EventEmitter();
//emitter.setMaxListeners(20);
//console.log("process.argv 값 : " + data);
var url_goto = "http://www.hsmoa.com/search?query=" + encodedData + "&from=navigation_query";

var requestOptions = {
    maxRedirects: 15,
    timeout: 5000
};

request(url_goto, requestOptions, function(error, response, html) {
    if(error) {throw error};
    
    //EventEmitter.setMaxListeners(15);
    const $ = cheerio.load(html);
    var requests = $('#list_ > a').slice(0,7).map(function(index, element){

        const name = $(this).find('div.listbox > div.detail > div.title').text().trim();
        const price = $(this).find('div.listbox > div.detail > div.price').text().trim();
        const img_url = $(this).find('div.listbox > div.thum > img').attr('src');
        const url_info= $(this).attr('href');
        var url_detail = "http://www.hsmoa.com" + url_info; 

        return requestDetailPage(name, price, img_url, url_detail);
    }).get();

    Promise.all(requests)
        .then(function() {
            var jsonData = JSON.stringify(list, null, 2);

            fs.writeFileSync('./webCrawling/output.json', jsonData, 'utf8');
            console.log('JSON file has been saved!');
        })
        .catch(function(error) {
            console.log('Error:', error);
        });
    
});

function requestDetailPage(name, price, img_url, url_detail) {
    return new Promise(function(resolve, reject) {
        request(url_detail, function(error, response, html) {
            if (error) {
                reject(error);
                return;
            }

            const $ = cheerio.load(html);
            var rowData = {};

            if($('#ProTab04').length) { //gsshop
                $('#ProTab04 > div.normalN_table_wrap.more > table > tbody > tr').each(function(index, element) {
                    const info = $(this).find('th').text().trim();
                    const info2 = $(this).find('td').text().trim();
                    //rowData.push({'info': info, 'info2' : info2});
                    rowData[info] = info2;
                });
                //console.log(rowData);
            }
            else if($('#ui_tab2').length) { //sinsegaetv
                $('#ui_tab2 > div.tab_cont.tab_details_info > div:nth-child(3) > div.desc_con > div > ul > li').each(function(index, element) {
                    const info = $(this).find('dl > dt').text().trim();
                    const info2 = $(this).find('dl > dd').text().trim();
                    //rowData.push({'info':info, 'info2': info2});
                    rowData[info] = info2;
                });

                //console.log(rowData);
            }
            else if($('#contents').length) { //롯데홈쇼핑
                $('#contents > div.detail_sec > div.division_product_tab.fixed > div.content_detail > div.wrap_detail.content2.on > div > div:nth-child(3) > table > tbody > tr').each(function(index, element) {
                    const info = $(this).find('th').text().trim();
                    const info2 = $(this).find('td').text().trim();
                    rowData[info] = info2;
                });
            }
            else if($('#_itemExplainAreaInfo').length) { //cj온스타일
                $('#_itemExplainAreaInfo > div.original_ex > div > table > tbody > tr').each(function(index, element) {
                    const info = $(this).find('th').text().trim();
                    const info2 = $(this).find('td').text().trim();
                    rowData[info] = info2;
                });
            }
            else if($('#tab_outside2').length) { //Kshop
                $('#tab_outside2 > div:nth-child(4) > div.area_body.clearfix._fold > div > table > tbody > tr').each(function(index, element) {
                    const info = $(this).find('th').text().trim();
                    const info2 = $(this).find('td').text().trim();
                    rowData[info] = info2;
                });
            }
            else if($('#tabDD2').length) { //하이마트
                $('#tabDD2 > div:nth-child(2) > div > div.hm-box-toggle__content.js-toggle-target-info-requied > div.hm-table1.hm-table1--tbody-th-bg-gray.hm-goods__info-table > table > tbody > tr').each(function(index, element) {
                    const info = $(this).find('th').text().trim();
                    const info2 = $(this).find('td').text().trim();
                    rowData[info] = info2;
                });
            }

            list.push({'name': name, 'price': price, 'img_url':img_url, 'goto_url': url_detail, 'detail': rowData});

            //console.log(list);

            resolve();
        });
    });
}