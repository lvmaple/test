function saveinfo(){

var info = getinfo();
alert(info);
    
}
//获取值
function getinfo(){
var key = "";
var value = "";
var data = "";
var table = $("#table");
var tbody = table.children();
var trs = tbody.children();
for(var i=1;i<trs.length;i++){
var tds = trs.eq(i).children();
for(var j=0;j<tds.length;j++){
if(j==0){
if(tds.eq(j).text()==null||tds.eq(j).text()==""){
return null;
}
key = "key\":\""+tds.eq(j).text();
}
if(j==1){
if(tds.eq(j).text()==null||tds.eq(j).text()==""){
return null;
}
value = "value\":\""+tds.eq(j).text();
}
}
if(i==trs.length-1){
data += "{\""+key+"\",\""+value+"\"}";
}else{
data += "{\""+key+"\",\""+value+"\"},";
}
}
data = "["+data+"]";
return data;
}
var clientWidth = document.documentElement.clientWidth;
var clientHeight = document.documentElement.clientHeight;
var div_left_width = 200;
var tempWidth = 0;
/**
* 描述：页面自适应
*/
$(window).bind("resize",function(){
resizeLayout();
});
function resizeLayout(){
try{
clientWidth = document.documentElement.clientWidth;
var div_left_width = $("#left").width()+11;
$("#cc").layout("resize");
$('#userquery').panel('resize',{width:clientWidth-div_left_width});
$('#10100801').datagrid('resize',{width:clientWidth-div_left_width});

$('#userrange').combobox({
width : $('#right').width() * 0.35
});
}catch(e){
}
}
function initResize(){
//自动适应页面大小
$(".layout-button-left").bind("click",function(){
$('#userquery').panel('resize',{width:clientWidth-28});
$('#10100801').datagrid('resize',{width:clientWidth-28});
$(".layout-button-right").bind("click",function(){
$('#userquery').panel('resize',{width:tempWidth});
$('#10100801').datagrid('resize',{width:tempWidth});
});
});
}
function tdclick(tdobject){
var td=$(tdobject);
td.attr("onclick", "");
//1,取出当前td中的文本内容保存起来
var text=td.text();
//2,清空td里面的内容
td.html(""); //也可以用td.empty();
//3，建立一个文本框，也就是input的元素节点
var input=$("<input>");
//4，设置文本框的值是保存起来的文本内容
input.attr("value",text);
input.bind("blur",function(){
var inputnode=$(this);
var inputtext=inputnode.val();
var tdNode=inputnode.parent();
tdNode.html(inputtext);
tdNode.click(tdclick);
td.attr("onclick", "tdclick(this)");
});
input.keyup(function(event){
var myEvent =event||window.event;
var kcode=myEvent.keyCode;
if(kcode==13){
var inputnode=$(this);
var inputtext=inputnode.val();
var tdNode=inputnode.parent();
tdNode.html(inputtext);
tdNode.click(tdclick);
}
}); 

//5，将文本框加入到td中
td.append(input);
var t =input.val();
input.val("").focus().val(t);
// input.focus();

//6,清除点击事件
td.unbind("click");
}
function addtr(){
var table = $("#Ltable");
var tr= $("<tr><td height='20px' onclick='tdclick(this)'>"+"</td><td height='20px' onclick='tdclick(this)'>"+"</td><td height='20px' align='center' onclick='deletetr(this)'><font size='2' color='red'>"+"删除"+"</font></td></tr>");
table.append(tr);
}
function deletetr(tdobject){
var td=$(tdobject);
td.parents("tr").remove();
}