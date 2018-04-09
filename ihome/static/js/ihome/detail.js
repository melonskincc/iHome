function hrefBack() {
    history.go(-1);
}

// 解析提取url中的查询字符串参数
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    // 获取详情页面要展示的房屋编号
    var queryData = decodeQuery();
    var houseId = queryData["id"];

    // 获取该房屋的详细信息
    $.get('/api/1.0/houses/detail/'+houseId,function (res) {
        if(res.re_code=='0'){
            render_template=template('house-image-tmpl',{'img_urls':res.data.house.img_urls,'price':res.data.house.price});
            $('.swiper-container').html(render_template);
            html=template('house-detail-tmpl',{'house':res.data.house});
            $('.detail-con').html(html);
            // 数据加载完毕后,需要设置幻灯片对象，开启幻灯片滚动
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });
            //如果不是自己发布的房源，即可预定按钮显示
            if (res.data.login_user_id != res.data.house.user_id){
                $('.book-house').show();
                $('.book-house').attr('href','/booking.html?hid='+res.data.house.hid);
            }
        }else {
            alert(res.msg);
            $('.book-house').hide();
        }
    });

});