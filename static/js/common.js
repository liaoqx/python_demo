//全选或取消全选
function selectAll(){
    var ctrl_box = document.getElementById("ctrl_box")
    var other_boxes = document.getElementsByName("selected")
    if(ctrl_box.checked)
        for(var i = 0;i < other_boxes.length;i++)
           other_boxes[i].checked = true
    else
       for(var i = 0;i < other_boxes.length;i++)
           other_boxes[i].checked = false
}

//点击删除时,检查用户是否勾选了待删选项
function checkSelection(){
    var ids_arr = new Array()
    var checked_boxes = document.getElementsByName("selected")
    for(var i = 0;i < checked_boxes.length;i++)
        if(checked_boxes[i].checked == true)
            ids_arr.push(checked_boxes[i].value)
    return ids_arr
}

//提交车辆信息时,拼接色系选项参数
function getColors(){
//alert("getColors")
    var checked_boxes = document.getElementsByName("color_list")
    var color_list = new Array()
    for (var i = 0; i < checked_boxes.length;i++){
        if(checked_boxes[i].checked == true){
            color_list.push(checked_boxes[i].value)
        }
    }
    if(color_list.length >= 1){
        var colors = document.getElementById('colors').value = color_list.join("")
        return true
    }else{
        alert("请选择该车型的色系!")
        return false
    }
}