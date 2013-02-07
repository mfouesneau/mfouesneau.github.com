<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
<head>
<title>Morgan Fouesneau- pIM</title>
<meta http-equiv="Content-type" content="text/html;charset=iso-8859-1" />
<meta name="language" content="en" />
<meta http-equiv="Content-Language" content="en" />
<meta name="keywords" content="" />
<link rel="stylesheet" media="screen" type="text/css" title="Design" href="style.css" />
</head>

<body>

<div id="top">
<p id="top_title">News</p>
<hr>
</div>

<h1><span class="caps">p</span>lot <span class="caps">IM</span>proved <span class="end">for IDL</span></h1>

<?php include("_menu.php");

function display_news($title, $date, $text)
	{
	$text = str_replace("::N::", "<br />", $text);
	$text = str_replace("::B::", "<b>", $text);
	$text = str_replace("::I::", "<i>", $text);
	$text = str_replace("::/B::", "</b>", $text);
	$text = str_replace("::/I::", "</i>", $text);
	echo '<div style="margin-bottom: 50px; border-left: 1px #CCCCCC dotted; padding-left: 10px;">';
	echo '<h2>'.$title.'</h2>';
	echo '<p style="text-align: right;">'.date('l, F d Y, g:i a', $date).'</p>';
	echo '<p>'.$text.'</p>';
	echo '</div>';
	}


if (isset($_GET['news_id']))
	{display_news($news[0][$_GET['news_id']], $news[1][$_GET['news_id']], $news[2][$_GET['news_id']]);}
else
	{
	for($i = 0 ; $i < $nnews ; $i++)
		{display_news($news[0][$i], $news[1][$i], $news[2][$i]);}
	}

?>

<?php include("_bottom.php"); ?>