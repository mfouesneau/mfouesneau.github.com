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
<p id="top_title">Online Help</p>
<hr>
</div>
<h1><span class="caps">p</span>lot <span class="caps">IM</span>proved <span class="end">for IDL</span></h1>



<?php include("_menu.php");


function display_function_doc($f, $d, $s, $a, $g, $gk) // name, description, syntax, args, graphics keywords id array
	{
	static $id = 0;
	echo '<div style="margin-bottom: 50px; border-left: 1px #CCCCCC dotted; padding-left: 10px;">';
	echo '<h2><a name="'.$id.'_name"></a>'.$f.'</h2>';
	if($a != '')
		{echo '<p><a href="#'.$id.'_description">Description</a> | <a href="#'.$id.'_syntax">Syntax</a> | <a href="#'.$id.'_args">Arguments</a>';}
	if($g != '')
		{echo ' | <a href="#'.$id.'_graphics">Graphics Keywords</a>';}
	echo '</p>';
	echo '<h3><a name="'.$id.'_description"></a>Description:</h3>';
	echo '<p class="function">'.$d.'</p>';
	if($s !='')
		{
		echo '<h3><a name="'.$id.'_syntax"></a>Syntax:</h3>';
		echo '<p class="function"><span class="function_name">'.$f.'</span>, '.$s.'</p>';
		}
	if($g != '')
		{
		echo '<h3>Graphics Keywords:</h3>';
		echo '<p class="function">' ;
		for ($i=0;$i<SIZEOF($g);$i++)
			{
			echo '[, '.$gk[1][$g[$i]].'] ';
			}
		echo '</p>';
		}
	if($a != '')
		{
		echo '<h3><a name="'.$id.'_args"></a>Arguments:</h3>';
		echo '<p class="function">'.$a.'</p>';
		}
	if($g != '')
		{
		echo '<h3><a name="'.$id.'_graphics"></a>Graphics Keywords Accepted:</h3>';
		echo '<p class="function">See <a
		href="http://idlastro.gsfc.nasa.gov/idl_html_help/Graphics_Keywords.html">Graphics
		Keywords</a> for the description of the following graphics and plotting keywords</p>';
		echo '<p class="function">' ;
		for ($i=0;$i<SIZEOF($g)-1;$i++)
			{
			echo $gk[0][$g[$i]].", ";
			}
		echo $gk[0][$g[$i]];
		echo '</p>';
		}
	echo '</div>';
	$id++;
	}

	
if (isset($_GET['f']))
	{display_function_doc($function[0][$_GET['f']], $function[1][$_GET['f']], $function[2][$_GET['f']], $function[3][$_GET['f']], $function[4][$_GET['f']], $gk);}
else
	{
	for($i=0 ; $i < $nfunctions ; $i++)
		{display_function_doc($function[0][$i], $function[1][$i], $function[2][$i], $function[3][$i], $function[4][$i], $gk);}
	}
?>


<?php include("_bottom.php"); ?>
