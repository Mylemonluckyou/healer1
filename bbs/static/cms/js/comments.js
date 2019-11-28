
$(function () {
   $('#add-comment-btn').click(function (event) {
       event.preventDefault();

       layer.prompt({title: '输入您要添加的评论，并确认', formType: 2}, function(text, index){


           bbsajax.post({
                   'url': '/cms/acomment/',
                   'data': {
                       'name':text
                   },
                   'success': function (data) {
                       if(data['code'] ==200){
                           layer.msg('添加成功')
                           window.location.reload();
                       }else{
                           // xtalert.alertInfo(data['message'])
                           layer.msg(data['message']);
                       }
                   }
               });


        layer.close(index);

    });



   });
});

//编辑板块
$(function () {
   $('.edit-comment-btn').click(function () {
       var self = $(this);
       var tr = self.parent().parent();
       var name = tr.attr('data-name');
       var comment_id = tr.attr('data-id');

       console.log(name,comment_id)


       var txt;
        var person = prompt("请输入评论：", name);
        if (person == null || person == "") {
                 txt = "用户取消输入";
        } else {
                // console.log(txt)
            bbsajax.post({
                   'url': '/cms/ucomment/',
                   'data': {
                       'comment_id': comment_id,
                       'name': person,
                   },
                   'success': function (data) {
                       if (data['code'] == 200) {
                           window.location.reload();
                       } else {
                           layer.msg(data['message'])
                       }
                   }
               });
            txt = "你好，" + person + "！今天过得好吗？";
            console.log('hello',name)
        }
   })
});


//删除板块
$(function () {
   $('.delete-comment-btn').click(function () {
       var self = $(this);
       var tr = self.parent().parent();
       var comment_id = tr.attr('data-id');

       bbsajax.post({
           'url': '/cms/dcomment/',
           'data': {
               'comment_id': comment_id
           },
           'success': function (data) {
               if (data['code'] == 200) {
                   window.location.reload();
               } else {
                   // xtalert.alertInfo(data['message'])
                   layer.msg(data['message'])
               }
           }
       });
   });
});