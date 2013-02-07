<?php
$password='';
if (isset($_POST['mdp']))
	{$password=$_POST['mdp'];}
if ($password=='#!pimonline')
	{
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
<title>Console d'administration</title>
<meta http-equiv="Content-type" content="text/html;charset=iso-8859-1" />
<meta name="language" content="fr" />
<link rel="stylesheet" media="screen" type="text/css" title="Design astrophy" href="style.css" />
</head>

<body>

<div id="top">
<p id="top_title">Welcome</p>
<hr>
</div>

<h1><span class="caps">p</span>lot <span class="caps">IM</span>proved <span class="end">for IDL</span></h1>

<?php include("_menu.php"); ?>

<h1>Admin MorganPlot</h1>

<form method="post" action="task.php?t=addnews" enctype="multipart/form-data">
<fieldset style="width:50%; margin: auto;">
<legend>News</legend>
<p>Title: <input type="text" name="title" size="50" /></p>
<p>Text<br /> <textarea rows="10" cols="55" name="text"></textarea></p>
<p><input type="submit" value="Submit" /></p>
</fieldset>
</form>
<p>To use bold font, enclose the text between ::B:: and ::/B::</p>
<p>To use italic font, enclose the text between ::I:: and ::/I::</p>
<p>PS: pIM is great ... almost as you are.</p>

<?php include("_bottom.php");
	}
else
	{
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
<head>
<title>Admin</title>
<meta http-equiv="Content-type" content="text/html;charset=iso-8859-1" />
</head>
<body>
<form method="POST" action="admin.php">
<p style="text-align:center; font-size: 12pt;">Password please:<br />
<input type="password" name="mdp" size="20" /><br />
<input type="submit" value="Submit" name="B1" /></p>
</form>
</body>
</html>
<?php } ?>
