// 主页面查看同义属性按钮
function clickOtherAttr(button){
    $bestAttr = button.parentElement.parentElement.getElementsByTagName('td')[1].textContent
    $domain = $("body > div > div > h3 > span").attr('value')
    $("#otherAttr > div.modal-dialog > div > div.modal-body > table > tbody").children().remove()
    $.ajax({url:"/api/getAttribute?type=1&domain="+$domain+"&bestAttr="+$bestAttr, success:function(data){
        if (data['status'] == 1){ alert('error'+'\n'+data['reason']); return };
        $.each(data['data'], function (i, result){
            add2otherAttr(i, result);
        });
        $("#otherAttr > div.modal-dialog > div > div.modal-body > table").attr('value', $bestAttr);
    }})
    $('#otherAttr').modal('toggle');
}

// 添加同义词属性到页面
function add2otherAttr(i, result){
    $num = i+1
    $tbody = $("#otherAttr > div.modal-dialog > div > div.modal-body > table > tbody")
    $tr = '<tr class="active"><td>'+$num+'</td><td>'+result+'</td><td><button type="button" class="btn btn-primary btn-sm btn-danger" onclick="deleteOtherAttr(this)">删除</button></td></tr>'
    $tbody.append($tr)
}

// 增加同义词推送到服务器，由$("#addOtherAttrEach").bind('click', function()调用
function manAdd2otherAttr(domain='person', otherAttr, fromAttr){
    $post_param = {'domain':domain, 'otherAttr':otherAttr, 'fromAttr':fromAttr}
    $.post("/api/addAttribute", $post_param, function(text, status){
        if (text['status'] == 1){ alert('error'+'\n'+data['reason']); return };
        if (status != 'success'){
            alert('添加失败'+'\n'+text)
        };
    })
}


// 同义词弹出页面中删除按钮
function deleteOtherAttr(button){
    $otherAttr = button.parentElement.parentElement.getElementsByTagName('td')[1].textContent;
    $domain = $("body > div > div > h3 > span").attr('value');
    mandeleteOtherAttr($domain, $otherAttr);
    delotherAttrStyle(button.parentElement.parentElement, $otherAttr);
}

// 设置同义词删除属性后的样式
function delotherAttrStyle(tr, otherAttr){
    tr.setAttribute('class', 'danger');
    tr.getElementsByTagName('td')[1].innerHTML = '<del>'+ otherAttr + '</del>';
}

// 同义词删除单条
function mandeleteOtherAttr(domain='person', otherAttr, type=1){
    if (type === 1){
        $post_param = {'domain':domain, 'otherAttr':otherAttr, 'type':type};
    }else if(type === 0){
        $post_param = {'domain':domain, 'bestAttr':otherAttr, 'type':type};
    };
    $.post("/api/deleteAttribute", $post_param, function(text, status){
        if (text['status'] == 1){ alert('error'+'\n'+data['reason']); return };
        if (status != 'success'){
            alert('删除失败'+'\n'+text)
        };
    })
}


// 主页面删除最优属性按钮
function delBestAttr(button){
    $("#delcfmModel > div.modal-dialog > div > div.modal-body").children().remove()
    $bestAttr = button.parentElement.parentElement.getElementsByTagName('td')[1].textContent;
    $("#delcfmModel > div.modal-dialog > div > div.modal-body").append("<p>您确认要删除 <b>"+$bestAttr+"</b> 吗？</p>")
    $('#delcfmModel').modal('toggle');
}

// 弹出删除确认框确认按钮，删除最优属性
function confirmDel(button){
    $domain = $("body > div > div > h3 > span").attr('value');
    $bestAttr = $("#delcfmModel > div.modal-dialog > div > div.modal-body > p > b").text();
    mandeleteOtherAttr($domain, $bestAttr, 0);
    $("body > div > div > table > tbody").children().remove();
    getBestAttr();
    $("#delcfmModel > div.modal-dialog > div > div.modal-body > p > b").text('');

}


// 主页面添加最优属性按钮
$("#addAttr").bind('click', function(){
    $('#addModel').modal('toggle');
})

// 主页面选择领域按钮
$("#selectDomainButton").bind('click', function(){
    $('#selectDomain').modal('toggle');
})

// 同义词弹出页面中添加按钮
$("#addOtherAttrEach").bind('click', function(){
    $num_last = $(this).parent().parent().prev().children('tbody').children().last().children().first().text().trim()
    if ($num_last){
        $num = parseInt($num_last) + 1;
    }else{
        $num = 1
    };
    // otherAttr
    $attr = $(this).parent().parent().children('input');
    if (!$attr.val()){
        alert('输入值为空！');
        return
    }
    $domain = $("body > div > div > h3 > span").attr('value');
    $fromAttr = $("#otherAttr > div.modal-dialog > div > div.modal-body > table").attr('value');
    manAdd2otherAttr($domain, $attr.val(), $fromAttr);
    $tr = '<tr class="info"><td>' + $num + '</td><td>' + $attr.val() + '</td><td><button type="button" class="btn btn-primary btn-sm btn-danger" onclick="deleteOtherAttr(this)">删除</button></td></tr>'
    $(this).parent().parent().prev().children("tbody").append($tr);
    $attr.val('');
    return
})

// 添加最优属性
$("#addModel > div.modal-dialog > div > div.modal-footer > button.btn.btn-primary").bind('click', function(){
    $bestAttr = $("#addModel > div.modal-dialog > div > div.modal-body > div:nth-child(1) > input").val();
    $otherAttrs = $("#addModel > div.modal-dialog > div > div.modal-body > div:nth-child(2) > input").val().split(' ');
    $domain = $("body > div > div > h3 > span").attr('value');
    for(var i=0;i<$otherAttrs.length;i++){
     $otherAttr = $otherAttrs[i];
     if (!$otherAttr){continue}
     manAdd2otherAttr($domain, $otherAttr, $bestAttr);
    };
    $("body > div > div > table > tbody").children().remove();
    $("#addModel > div.modal-dialog > div > div.modal-body > div:nth-child(1) > input").val('');
    $("#addModel > div.modal-dialog > div > div.modal-body > div:nth-child(2) > input").val('')
    getBestAttr();


})


// 主页第一次加载
$(document).ready(function(){
    getBestAttr();
})

// 根据页码获取最优属性
function getBestAttr(domain='person', pn=1){
    $domain = $("body > div > div > h3 > span").attr('value');
    $.ajax({ url: "/api/getAttribute?domain="+domain+"&pn="+pn, beforeSend: showLoading() ,success: function(data){
        hiddenLoading();
        if (data['status'] == 1){ alert('error'+'\n'+data['reason']); return };
        $.each(data['data'], function (i, result){
            add2bestAttr(i, result);
        })
      }});
}


function showLoading(){
 $("body > div > div > table").after('<div id="loading"><img src="../static/box.gif"></div>');
}

function hiddenLoading(){
    $("#loading").remove();
}

// 添加最优属性到主页面，获取最优属性调用此函数
function add2bestAttr(i, bestAttr){
    $tbody = $("body > div > div > table > tbody")
    $num = i + 1
    $tr = '<tr class="active"><td>'+$num+'</td><td>'+bestAttr+'</td><td><button id="getOtherAttr" type="button" class="btn btn-primary btn-sm" data-target="#otherAttr" onclick="clickOtherAttr(this)">查看</button><button type="button" class="btn btn-primary btn-sm btn-danger" onclick="delBestAttr(this)">删除</button></td></tr>'
    $tbody.append($tr)
}


// 页码点击
$("body > div > div > nav > ul #page").children().bind('click', function (){
    $page = $(this).text();
    $("body > div > div > table > tbody").children().remove()
    $("body > div > div > nav > ul > li:nth-child(8) > b").text($page);
    $domain = $("body > div > div > h3 > span").attr('value');
    getBestAttr($domain, $page);
})


// 指定页面跳转
$('body > div > div > nav > ul > li > input').blur(function(){
    $page = $(this).val();
    if (parseInt($page)){
        $page = parseInt($page);
        $("body > div > div > table > tbody").children().remove();
        $("body > div > div > nav > ul > li:nth-child(8) > b").text($page);
        $domain = $("body > div > div > h3 > span").attr('value');
        getBestAttr($domain, $page);
        }
})

// 搜索按钮
function search(button){
    $bestAttr = button.parentElement.parentElement.getElementsByTagName('input')[0].value;
    if (!$bestAttr){alert('nothing!');return }
    $domain = $("body > div > div > h3 > span").attr('value')
    $.ajax({url:"/api/getAttribute?type=1&domain="+$domain+"&bestAttr="+$bestAttr, beforeSend: showLoading(), success:function(data){
        if (data['status'] == 1){ alert('error'+'\n'+data['reason']);
            $("body > div > div > table > tbody").children().remove();
            getBestAttr();
            return
        };
        hiddenLoading();
        $tbody = $("body > div > div > table > tbody");
        $tbody.children().remove();
        $tr = '<tr class="active"><td>'+1+'</td><td>'+$bestAttr+'</td><td><button type="button" class="btn btn-primary btn-sm" data-target="#otherAttr" onclick="clickOtherAttr(this)">查看</button><button type="button" class="btn btn-primary btn-sm btn-danger" onclick="delBestAttr(this)">删除</button></td></tr>'
        $tbody.append($tr);
    }});
    $("body > div > div > form > div > input").val('');
}

// // 上下页按钮
function lastnextPage(button, a){
    $currPage = $("body > div > div > nav > ul > li:nth-child(8) > b").text()
    $getPage = parseInt($currPage) + a
    if ($getPage < 1){return};
    $domain = $("body > div > div > h3 > span").attr('value');
    $("body > div > div > nav > ul > li:nth-child(8) > b").text($getPage);
    $tbody = $("body > div > div > table > tbody").children().remove();
    getBestAttr($domain, $getPage);
}


// 当同义属性删除完之后，点击关闭按钮会刷新主页面的最优属性表格
$("#otherAttr > div.modal-dialog > div > div.modal-footer > button").bind('click', function(){
    $tbody = $('#otherAttr > div.modal-dialog > div > div.modal-body > table > tbody');
    if ($tbody.children('.info').length != 0){return};
    $page = $("body > div > div > nav > ul > li:nth-child(8) > b").text();
    $domain = $("body > div > div > h3 > span").attr('value');
    $tbody = $("body > div > div > table > tbody").children().remove();
    getBestAttr($domain, $page);
})


