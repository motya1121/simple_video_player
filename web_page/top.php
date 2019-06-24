<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <title>home video page</title>
    <?php
    # ini_set('display_errors', "On");
    require("web_page_conf.php");
    if ($is_open == false) {
        exit;
    }

    $useragents = array('iPhone', 'iPod', 'Android', 'dream', 'CUPCAKE', 'blackberry9500', 'blackberry9530', 'blackberry9520', 'blackberry9550', 'blackberry9800', 'webOS', 'incognito', 'webmate');
    $devise_type = "pc";
    foreach ($useragents as $useragent) {
        if (strpos($_SERVER['HTTP_USER_AGENT'], $useragent) !== false) {
            $devise_type = "mobile";
        }
    }
    if ($devise_type == "pc") {
        echo '<link rel="stylesheet" type="text/css" href="style_pc.css">';
    } else {
        echo '<link rel="stylesheet" type="text/css" href="style_mobile.css">';
    }

    #change favorite
    if (!empty($_GET["sha1"]) && !empty($_GET["favorite"])) {
        $json_file = "videos.json";
        if (file_exists($json_file)) {
            $json = file_get_contents($json_file);
            $video_datas = json_decode($json, true);
            $index_count = 0;
            foreach ($video_datas as $video_data) {
                if ($video_data["sha1"] == $_GET["sha1"]) {
                    if ($_GET["favorite"] == "True") {
                        $video_datas[$index_count]["is_favorite"] = true;
                    } else {
                        $video_datas[$index_count]["is_favorite"] = false;
                    }
                }
                $index_count += 1;
            }
        }
        $json = fopen($json_file, 'w');
        fwrite($json, json_encode($video_datas));
        fclose($json);
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
                <form action="top.php" method="get">
                    <H3>Search</H3>
                    <input type="text" name="search" style="width:90%; box-sizing:border-box" maxlength="100" placeholder="検索文字列" value="<?php if (!empty($_GET["search"])) {
                                                                                                                                                echo $_GET["search"];
                                                                                                                                            } ?>"> <br>
                    <H3>並び順</H3>
                    <input type="checkbox" name="option[]" value="1" <?php if (in_array("1", $_GET["option"])) {
                                                                            echo ' checked="checked"';
                                                                        } ?>>再生回数
                    <input type="checkbox" name="option[]" value="2" <?php if (in_array("2", $_GET["option"])) {
                                                                            echo ' checked="checked"';
                                                                        } ?>>長い
                    <input type="checkbox" name="option[]" value="3" <?php if (in_array("3", $_GET["option"])) {
                                                                            echo ' checked="checked"';
                                                                        } ?>>短い
                    <input type="checkbox" name="option[]" value="4" <?php if (in_array("4", $_GET["option"])) {
                                                                            echo ' checked="checked"';
                                                                        } ?>>好き
                    <br><input type="submit" value="検索">
                </form>
            </div>
        </div>
        <div class="contents_main">
            <?php
            #sort videos
            $video_datas = video_sort($video_datas, $_GET["option"], $_GET["search"]);

            #display videos
            $count = 1;
            foreach ($video_datas as $video_data) {
                if ($video_data["exists_video_file"] == false) {
                    continue;
                }
                $video_dir_path = "video_contents/" . sha1($video_data["video_dir_path"]);
                $img_path = substr($video_data["video_file_name"], 0, strrpos($video_data["video_file_name"], ".")) . ".jpg";
                echo '<div class="contents_main_video" id="' . $video_data["sha1"] . '">';
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
                if ($video_data["is_favorite"] == true) {
                    echo '<BR><a onclick="change_favorite(\'' . $video_data["sha1"] . '\',\'False\')"><font color="red">&#9829;</font></a>';
                } else {
                    echo '<BR>お気に入り<a onclick="change_favorite(\'' . $video_data["sha1"] . '\',\'True\')"><font color="red">&#9825;</font></a>';
                }
                echo '</div>';
                echo '</div>';
                if (20 < $count) {
                    break;
                } else {
                    $count++;
                }
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

    function change_favorite(sha1, setting) {
        location.href = 'top.php?sha1=' + sha1 + '&favorite=' + setting + '#' + sha1;
    }
</script>
<?php
function video_sort($video_datas, $options, $search_str)
{
    //option
    foreach ($options as $option) {
        if ($option == "4") { //お気に入り
            foreach ($video_datas as $key => $value) {
                if ($value["is_favorite"] == false) {
                    //削除実行
                    unset($video_datas[$key]);
                }
            }
            array_values($video_datas);
        }
        if ($option == "2" || $option == "3") { //長さ
            foreach ($video_datas as $key => $value) {
                $view_count[$key] = $value['video_length'];
            }
            if ($option == "2") {
                array_multisort($view_count, SORT_DESC, $video_datas);
            } else if ($option == "3") {
                array_multisort($view_count, SORT_ASC, $video_datas);
            }
        }
        if ($option == "1") { //再生回数
            foreach ($video_datas as $key => $value) {
                $view_count[$key] = $value['view_count'];
            }
            array_multisort($view_count, SORT_DESC, $video_datas);
        }
    }
    if (empty($options)) {
        foreach ($video_datas as $key => $value) {
            $view_count[$key] = rand(0, 100000);
        }
        array_multisort($view_count, SORT_ASC, $video_datas);
    }

    //search
    if (!empty($search_str)) {
        foreach ($video_datas as $key => $value) {
            if (strpos($value["video_file_name"], $search_str) === false) {
                //削除実行
                unset($video_datas[$key]);
            }
        }
        array_values($video_datas);
    }


    return $video_datas;
}
?>

</html>