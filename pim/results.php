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
<p id="top_title">Search</p>
<hr>
</div>

<h1><span class="caps">p</span>lot <span class="caps">IM</span>proved <span class="end">for IDL</span></h1>

<?php include("_menu.php");

if (!isset($_POST['search']))
	{die("Error");}

$kw = htmlspecialchars($_POST['search']);
$pattern = '/'.$kw.'/i';

for($i = 0 ; $i < $nfunctions ; $i++)
	{
	$f = preg_match($pattern, $function[0][$i]);
	$d = preg_match($pattern, $function[1][$i]);
	$a = preg_match($pattern, $function[2][$i]);
	$g = preg_match($pattern, $function[3][$i]);
	$index = $f*25+$d*2.5+$a+$g;
	if($index != 0)
		{
		$res[0][] = $i; // functions id
		$res[1][] = $index; // relevance index
		}
	}



$nresults = SIZEOF($res[0]);

echo '<p>Search <span style="font-style: italic;">'.$kw.'</span>: ';

if($nresults == 0)
	{echo 'No results</p>';}
else
	{
	array_multisort($res[1],SORT_DESC, $res[0]);
	$results = $res[0];
	if($nresults == 1)
		{$plural = '';}
	else
		{$plural = 's';}
	
	echo '('.$nresults.' result'.$plural.')</p>';
	
	for($i = 0 ; $i < $nresults ; $i++)
		{
		echo '<div style="margin-bottom: 30px">';
		echo '<p style="margin: 0;"><a href="help.php?f='.$results[$i].'">'.$function[0][$results[$i]].'</a></p>';
		echo '<p style="margin: 0; padding-left: 20px;">'.$function[1][$results[$i]].'</p>';
		echo '</div>';
		}
	}
?>

<?php include("_bottom.php"); ?>
