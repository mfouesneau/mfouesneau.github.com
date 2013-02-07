<?php 
if ($_GET['t']=="addnews")
	{
	function antiquote($text)
		{
		$text = strip_tags($text);
		$text = str_replace("<br />", "::N::", nl2br($text));
		$text = str_replace('\\','',$text); // remove strange things
		$text = htmlspecialchars($text,ENT_QUOTES);
		return $text;
		}

	$title = antiquote($_POST['title']);
	$date = time();
	$text = antiquote($_POST['text']);

	$feed = 'news.xml';

	$fp = fopen($feed, "r+");
	
	$tmp = fseek($fp, -8, SEEK_END); // move pointer back to the begining of last line
	$new = "<news>\n<title>".$title."</title>\n<date value=\"".$date."\" />\n<text>\n".$text."</text>\n</news>\n\n</data>";
	fputs($fp, $new);
	fclose($fp);

	header("Location: index.php");
	}
	
echo "<html><body></body></html>";

?>
