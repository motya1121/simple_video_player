<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <title>home video page</title>
    <link rel="stylesheet" type="text/css" href="style_pc.css">
    <?php
	ini_set('display_errors', "On");
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
            <h1><a href="top.html" class="noline">home video page</a></h1>
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
				print_r($video_data);
				echo "<BR>";
				echo ' <div class="contents_main_video">';
				echo '<div class="contents_main_video_thumbnail">';
				echo '<img src="test_video001.jpg" class="contents_main_video_thumbnail">';
				echo '</div>';
				echo '<div class="contents_main_video_description">';
				echo '概要';
				echo '</div>';
				echo '</div>';
			}
			?>
        </div>
    </div>
    <div class="bottom">
        <a href="top.html">Home video page!</a>
    </div>
</body>

</html> 