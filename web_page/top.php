<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <title>home video page</title>
    <link rel="stylesheet" type="text/css" href="style_pc.css">
    <?php
    require("web_page_conf.php");
    if ($is_open == false) {
        exit;
    }

    $json_file = "videos.json";
    if (file_exists($json_file)) {
        $json = file_get_contents($json_file);
        $video_datas = json_decode($json, true);
    } else {
        echo "データがありません";
    }
    ?>
</head>

<body bgcolor="#FAFAFA">
    <div class="header">
        <div class="header_rogo">
            <h1><a href="top.php" class="noline">home video page</a></h1>
        </div>
    </div>
    <div class="contents">
        <div class="contents_panel">
            <div class="contents_panel_search">
                Search
                <form action="top.html" method="get">
                    <input type="text" name="search" style="width:90%; box-sizing:border-box" maxlength="100" placeholder="検索文字列"> <br><input type="submit" value="検索">
                </form>
            </div>
        </div>
        <div class="contents_main">
            <?php
            foreach ($video_datas as $video_data) {
                $video_dir_path = "video_contents/" . sha1($video_data["video_dir_path"]);
                $img_path = substr($video_data["video_file_name"], 0, strrpos($video_data["video_file_name"], ".")) . ".jpg";
                echo '<div class="contents_main_video">';
                echo '<div class="contents_main_video_thumbnail">';
                echo '<img src="' . $video_dir_path . '/' . $img_path . '" class="contents_main_video_thumbnail" onclick="jump_video_page(\'' . $video_data["sha1"] . '\')">';
                echo '</div>';
                echo '<div class="contents_main_video_description">';
                echo '<H2  onclick="jump_video_page(\'' . $video_data["sha1"] . '\')">' . substr($video_data["video_file_name"], 0, strrpos($video_data["video_file_name"], ".")) . '</H2>';
                echo '長さ:  ' . (int)($video_data["video_length"] / 60) . ':' . $video_data["video_length"] % 60;
                echo '<BR>再生回数:' . $video_data["view_count"] . '回';
                echo '<BR>タグ:';
                if (count($video_data["tags"]) != 0) {
                    foreach ($video_data["tags"] as $tag) {
                        echo $tag . ',';
                    }
                }
                echo '</div>';
                echo '</div>';
            }
            ?>
        </div>
    </div>
    <div class="bottom">
        <a href="top.php">Home video page!</a>
    </div>
</body>
<script>
    function jump_video_page(sha1) {
        location.href = 'watch.php?sha1=' + sha1;
    }
</script>

</html> 