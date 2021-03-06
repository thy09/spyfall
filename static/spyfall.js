var rules = '<h2>游戏规则</h2>' + 
        '<h3>基本配置</h3>' + 
        '<p>每一盘游戏会被分配某些场景中的一个，大部分玩家会在这个场景中扮演某个角色。</p>' + 
        '<p>例如: 大学的教授/学生/看门人etc。</p>' + 
        '<p>少数玩家是间谍，并不知道场景是什么。</p>' + 
        '<h3>游戏目标</h3>' + 
        '<p>间谍的目标是找到这个场景或在限定时间内不被发现，其他人的目标是找出所有的间谍。</p>' + 
        '<h3>游戏流程</h3>' + 
        '<p>从任意玩家开始，他可以向任意另一名玩家发问，被问的玩家必须回答。</p>' + 
        '<p>然后被问的玩家再选择一名其他玩家进行发问（但不能选择刚才问你的人）。</p>' + 
        '<h3>游戏结算</h3>' + 
        '<p>任意时刻任意玩家(包括间谍)可以提出指认某人为间谍，若(总人数-间谍最大数量)个人同意指认，则被指认的人亮明身份。</p>' + 
        '<p>1. 指认错误，间谍方直接获胜，每个间谍得2分</p>' + 
        '<p>2. 指认正确，则非间谍方获胜，被指认的间谍外所有人得1分(其余间谍也得分)，指出者得2分</p>' + 
        '<p>3. 任意间谍任意时刻可跳出来指认地点，此时其他所有间谍也必须同时亮明身份，每个间谍指认一个地点，若至少有一名间谍指认正确，则间谍方获胜各得2分</p>' + 
        '<p>4. 设置时限(8人局建议8分钟)，到时限强制开始指认，若无法统一意见则间谍方获胜得2分。</p>' + 
        '<p>每次玩多盘(一般设定为5)，最后统计总分。</p>' + 
        '<h3>变体规则</h3>' + 
        '<p>变体规则1: 允许0个间谍存在，若所有人一致同意无间谍，且确实无间谍，则所有人共同胜利。提出无间谍者得1分。</p>' + 
        '<p>变体规则2: 发现一个间谍后，若还存在其他间谍，游戏继续进行，直到所有间谍都被找到/时间到/指认错误</p>' + 
        '<p>变体规则3: 每次指认时只需要过半数人同意指认即让被指认的人亮明身份</p>' + 
        '<p>变体规则4: 一个间谍跳出来时其他间谍可保持沉默, 若间谍指认地点错误，则该间谍被移出游戏，其余间谍继续参与游戏。间谍指认得分为留下了的间谍数量，其余间谍得1分</p>' + 
        '<p>变体规则5: 在4的基础上，存在一个地点为"间谍学校"，此时间谍看到的间谍数量是错误的，所有人都是间谍，但流程按照看到的虚假间谍数量为准。</p>';
var new_game = function(){
    var count = parseInt($("#count").val());
    var upper = parseInt($("#upper").val());
    var lower = parseInt($("#lower").val());
    var locid = $("#locid").val();
    var scenecount = parseInt($("#scenecount").val());
    var spyschool = $("#spyschool").val();
    if (lower > upper){
        alert("下限不能超过上限!");
        return;
    }
    if (upper > count/2){
        alert("间谍人数不能超过总人数的一半!");
        return;
    }
    var url = "./create?count="+count+"&upper="+upper+"&lower="+lower+"&locid="+locid + "&scenecount="+scenecount+"&spyschool="+spyschool;
    window.location.href = url;
}
var get_my_role = function(players, roles, scene, idx, spy_count){
    var div = $("<div class='p'></div>").text("编号"+idx+"的身份是:" + players[idx]);     
    $(".words").prepend(div);
    if (players[idx].indexOf("Spy")<0){
        $(".words").prepend($("<p>当前场景为: "+ scene +"</p>"))
        $(".words").append($("<h3>该场景角色如下</h3>"));
        for (var j in roles){
            var div = $("<p></p>").text(roles[j]);
            $(".words").append(div);
        }
    }else{
        $(".words").append($("<p>共有"+spy_count+"名间谍</p>"));
    }
}
var add_players = function(players, roles, scenes, scene, spy_count, occupied){
    for (var i in players){
        var player = players[i];
        var div = $("<div></div>").addClass("word").attr("id", i).html("<p>" + i + "号</p>");
        $(".words").append(div);
    }
    $(".words").append("<div style='clear:both'></div>");
    $(".words .word").each(function(idx, elm){
        if (occupied[idx]){
            $(elm).addClass("occupied");
            return;
        }
        $(elm).click(function(){
            var idx = parseInt($(elm).attr("id"));
            if (!confirm("确定选择"+idx+"号？")){
                return;
            }
            $.get("/sit"+location.search+"&idx="+idx,"", function(res){
                if (res.status != "success"){
                    if (res.status == "OCCUPIED"){
                        alert(idx+"号已经被别人选啦!");
                        $(elm).addClass("occupied");
                        $(elm).unbind("click");
                    }else{
                        alert(res.status);
                    }
                    return;
                }
                $(".words div").remove();
                get_my_role(players, roles, scene, idx, spy_count);
            });
        });
    });
}
$(document).ready(function(){
    $(".rules").html(rules);
    $.get("/status"+location.search,"",function(data){
        var game = data.game;
        console.log(game);
        $("title").text("Spyfall:"+game.id);
        if (data.my_idx !== undefined){
            get_my_role(game.players, game.roles, game.loc, data.my_idx, game.spy_count);
        }else{
            add_players(game.players, game.roles, game.scenes, game.loc, game.spy_count, game.occupied);
        }
        var max_count = 30;
        var max_scene = 50;
        for (var i=2;i<=max_count;i++){
            $("#count").append($("<option value='"+i+"'>"+i+"</option>"));
        }
        for (var i=1;i<=max_count/2;i++){
            $("#upper").append($("<option value='"+i+"'>"+i+"</option>"));
        }
        for (var i=0;i<=max_count/2;i++){
            $("#lower").append($("<option value='"+i+"'>"+i+"</option>"));
        }
        for (var i=2;i<=max_scene;i++){
            $("#scenecount").append($("<option value='"+i+"'>"+i+"</option>"));
        }
        $("#count").val(game.count);
        $("#upper").val(game.upper);
        $("#lower").val(game.lower);
        $("#scenecount").val(game.scenecount);
        $("#spyschool").val(game.spyschool);
        var locids = ["zh-cn-26", "zh-tw-52"];
        for (var i in locids){
            $("#locid").append($("<option value='"+locids[i]+"''>"+locids[i]+"</option>"));
        }
        $("#locid").val(game.locid);
        var h = document.body.clientWidth/30;
        $(".word").css("font-size",h);
        $(".word p").css("height",h);
        $(".hint").append($("<h3>可能场景列表如下(点击展开角色)</h3>"));
        for (var j in game.scenes){
            var div = $("<div class='scene'></div>").text(game.scenes[j]);
            var scene_vals = game.scenes[j].split(":")
            var scene_key = scene_vals[0];
            (function(scene, locid, div){
                div.click(function(){
                    if (div.find(".role").length > 0){
                        div.find(".role").toggleClass("hidden");
                        return;
                    }
                    var url = "/roles?locid="+game.locid+"&scene="+scene;
                    $.get(url,"", function(data){
                        console.log(data);
                        for (var i in data){
                            div.append($("<p class='role'></p>").text(data[i]));
                        }
                    });
                });
            })(scene_key, game.locid, div);
            $(".hint").append(div);
        }
        $(".hint").append("<p>分享此页面给朋友们即可开始玩耍！</p>");
    });
});
