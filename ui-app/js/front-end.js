/*
#   Copyright 2019 NEC Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
*/

var location_host = window.location.hostname;
var location_prot = window.location.protocol;
var api_url_base = location_prot + "//" + location_host + ":" + api_port;

function getPriceLoop(currency)
{
  // console.log(".productList");
  // console.log($(".productList").children());
  $(".productList").children().each(function(idx, elem) {
    // console.log("element");
    // console.log(elem);
    getPriceEachOne(elem, currency);
  });
}

function getPriceEachOne(elem, currency)
{
    var item_id = elem.id.split('-')[1];
    console.log($(elem));
    console.log("item_id: " + item_id);

    // API呼び出し
    new Promise(function(resolve, reject) {

        // APIの呼び出し
        console.log("CALL : Get Price");
        api_param = {
          "type": "GET",
          "url": api_url_base + "/goods/" + item_id + "/" + currency,
          dataType: "json",
        }

        $.ajax(api_param).done(function(data) {
          console.log("DONE : GetPrice");
          console.log("--- data ----");
          console.log(JSON.stringify(data));
          // 成功
          var goods_list = data['goods'];

          if(goods_list.length == 0){
            reject();
          }

          item = goods_list[0];
          console.log(item);

          $(elem).find('.productInfo').find('.name').html(item.name);
          var strPrice = "";
          for(var j = 0; j < item.price.length; j++){
            if (j != 0) strPrice = strPrice + "<br>";
            strPrice = strPrice + item.price[j]['formated_value'];
          }
          console.log(strPrice);
          $(elem).find('.productInfo').find('.price').html(strPrice);

          $(elem).find('.imgBox').find('a').html('<img src="./img/shirt.png"></img>');
          console.log(elem);

          console.log("Set Finish : GetPrice");

          resolve();
        }).fail(function() {
          console.log("FAIL : GetPrice");
          // 失敗
          reject();
        });

      }).then(() => {
        console.log('Complete !!');
      }).catch(() => {
        // 実行中ダイアログ表示
        console.log('Fail !!');
      });

}

$(function() {
  // プルダウンの初期値"YEN"をセット
  getPriceLoop("YEN");
});

$(function() { 
  $('select').change(function() {
    // プルダウンの選択値をセット
    getPriceLoop($(this).val());
  });
});
