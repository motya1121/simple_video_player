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
    # check exist GET data
    if (empty($_GET["sha1"])) {
        header('Location: top.php');
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
            $index_count = 0;
            foreach ($video_datas as $video_data) {
                if ($video_data["sha1"] == $_GET["sha1"]) {
                    $video_dir_path = "video_contents/" . sha1($video_data["video_dir_path"]);
                    echo '<H2>' . substr($video_data["video_file_name"], 0, strrpos($video_data["video_file_name"], ".")) . '</H2>';
                    echo '<video src="' . $video_dir_path . '/' . $video_data["video_file_name"] . '" controls></video>';
                    $video_datas[$index_count]["view_count"] += 1;
                }
                $index_count += 1;
            }

            $json = fopen($json_file, 'w');
            fwrite($json, json_encode($video_datas));
            fclose($json);
            ?>
        </div>
    </div>
    <div class="bottom">
        <a href="top.php">Home video page!</a>
    </div>
</body>


</html> 