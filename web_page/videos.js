var write_canvas_list=[];
function getJSON(path) {
    var obj;
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
      if(req.readyState == 4 && req.status == 200){
        obj =JSON.parse(req.responseText);
      }
    };
    req.open("GET", path, false);
    req.send(null);
    return (obj);
}

function write_video_list(videos,write_videoid_list){
    target = document.getElementById("contents_main");
    var i=0;
    videos["videos"].forEach(function(video){
      container="<table><tbody><tr><td>";
      if (write_videoid_list.indexOf(video["id"])>=0){
        if (video["thumbnai"]==null){
          container+='<a href="watch.html?id='+video["id"]+'"><canvas id="cv'+i+'" width="256" height="144"></canvas></a>';
          write_canvas_list.push(["cv"+i,video["title"]]);
          i+=1;
        }else{
          path=assembly_path(video["path"]);
          container+='<a href="watch.html?id='+video["id"]+'"><img border="0" src="'+path+video["thumbnai"]+'" width="256" height="144" alt="イラスト1"></a>';
        }
        container+="</td><td>";
        container+='<a href="watch.html?id='+video["id"]+'"><b>'+video["title"]+'</b></a>&nbsp;'+video["length"]+'秒<br>';
        container+=video["commentary"]+"<br>";
        container+=video["tags"];
        container+="</td></tr></tbody></table>";
        target.insertAdjacentHTML ('beforeend',container);
      }
    }
  );
}

function write_canvas(id,string) {
  var canvas = document.getElementById(id);
  if (canvas.getContext) {
    var context = canvas.getContext('2d');
    context.fillStyle = "black";
    context.font = "40px 'ＭＳ ゴシック'";
    context.fillText(string, 0, 75);

  }
}

function search_video(search_str){
  var write_videoid_list=[];
  if (search_str==null){
    videos["videos"].forEach(function(video){
      write_videoid_list.push(video["id"]);
    }
  )
  }else{
    videos["videos"].forEach(function(video){
      if(video["title"].indexOf(search_str) != -1){
        write_videoid_list.push(video["id"]);
      }
    })
  }
  return (write_videoid_list);
}

function write_video(videos,id){
    target = document.getElementById("contents_main");
    videos["videos"].forEach(function(video){
        if (video["id"]==id){
          path=assembly_path(video["path"]);
          path+=video["f_name"];
          container='<video src="'+path+'" width=100% controls></video>';
          target.insertAdjacentHTML ('beforeend',container);
        }
    })
}

function assembly_path(path_list){
  var path="";
  for(var i=0;i<path_list.length;i++){
    path+=path_list[i]+"/";
  }
  return (path);
}