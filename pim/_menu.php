<!-- define the left panel -->
<div style="float: left; width: 300px;">

<?php
$pimfile = "pim.tar.gz"; // name of the downloadable file (with relative path)
$nlast_news = 3; // nb of visible news
$short_news_title_length = 30; // ~ nb of char of the short title for the news displayed in the left panel


/////////////////////////////////////////////////////
// FUNCTIONS DEFINITIONS
// Name
$function[0] = array(
		"pIM", 
		"OpIM",
		"pIMset",
		"pIMsetAxis",
		"pIMShareAxis",
		"pIMsetCurve",
		"pIMdelCurve",
		"pIMaddView",
		"pIMdelView",
		"pIMselectView",
		"pIMunselectView",
		"pIMsetLegend",
		"pIMaddNote",
		"pIMsetNote",
		"pIMdelNote",
		"pIM2PS",
		"pIMpalette",
		"PSym Internal Catalog"
		);
// Description
$function[1] = array(
		"The pIM procedure draws graphs of vector arguments. If one parameter is used, the vector parameter is plotted on the ordinate versus the point number on the abscissa. To plot one vector as a function of another, use two parameters. pIM can also be used to generate a specific sub-figure that will be completed later.", 
		"The OpIM procedure plots vector data over a previously-drawn plot. It differs from pIM only in that it does not generate a new figure. Instead, it uses the previous established by the most recent call to pIM or the current selection from pIMselectView and simply add a plot of the data on the existing axis.",
		"Change Current figure properties. You may prefer pIMsetView to this procedure.",
		"Create, delete or change properties of a given axis",
		"Create a share axis between two figures. This will make those figures to be side by side with a common axis. Any modification of this axis from one or the other figure will affect also the second.",
		"Modify properties of one or multiple curves",
		"Delete selected curve(s)",
		"add a new sub-figure to the current graphics and also plot the first curve of this view if provided.",
		"Delete a sub-figure from the current graphics. All associated data are also deleted.",
		"Select a sub-figure on which you want to have an action. By default, the last added 'View' is active",
		"Unselect a sub-figure and thus avoid further changes until a new selection.",
		"Modify current view legend parameters.",
		"Add a note to the current view.",
		"Modify selected note(s) from the current view.",
		"Delete selected note(s)",
		"Aka pIMtoPS, Export the current graphics to a Postscript file, and provide some help to configure the Postscript device",
		"The pIMpalette function creates an internal color bar widget. This widget is a color selector where the table color displayed is the table used during the Postscript conversion. It displays on the right hand side the selected color and its hexadecimal value. You can call pIMpalette as a procedure in order to look at a color value or as a function within argument list.",
		"pIM also integrates an internal symbol catalog more complete
		than the original IDL catalog. Of course, this catalogs keeps
		IDL's symbol with the same number but also includes a lot more
		beginning from a circle with the number 9. So you can use this
		catalog directly into pIM as you usually do in IDL. All symbol
		commands are using this internal catalog. See the symbol list
		above to see what's available.<br>
			
<br><img src='pics/pimsymbols.png' alt='coucou toto' /><br>
<table style='width:500px;margin-left:auto;margin-right:auto'>
 <tr> <td>  0  </td><td>  No symbol 			 </td> <td style='padding-left:50px;'>  24 </td><td>   Filled bowtie                     </td>  </tr>
 <tr> <td>  1  </td><td>  Plus sign                      </td> <td style='padding-left:50px;'>  25 </td><td>   Standing Bar                      </td>  </tr>
 <tr> <td>  2  </td><td>  Asterisk                       </td> <td style='padding-left:50px;'>  26 </td><td>   Filled Standing Bar               </td>  </tr>
 <tr> <td>  3  </td><td>  Dot (period)                   </td> <td style='padding-left:50px;'>  27 </td><td>   Laying Bar                        </td>  </tr>
 <tr> <td>  4  </td><td>  Open diamond                   </td> <td style='padding-left:50px;'>  28 </td><td>   Filled Laying Bar                 </td>  </tr>
 <tr> <td>  5  </td><td>  Open upward triangle           </td> <td style='padding-left:50px;'>  29 </td><td>   Hat up                            </td>  </tr>
 <tr> <td>  6  </td><td>  Open square                    </td> <td style='padding-left:50px;'>  30 </td><td>   Hat down                          </td>  </tr>
 <tr> <td>  7  </td><td>  X                              </td> <td style='padding-left:50px;'>  31 </td><td>   Hat right                         </td>  </tr>
 <tr> <td>  8  </td><td>  &lt;Keep USERSYM&gt;           </td> <td style='padding-left:50px;'>  32 </td><td>   Hat down                          </td>  </tr>
 <tr> <td>  9  </td><td>  Open circle                    </td> <td style='padding-left:50px;'>  33 </td><td>   Big cross                         </td>  </tr>
 <tr> <td>  10 </td><td>  Histogram style plot           </td> <td style='padding-left:50px;'>  34 </td><td>   Filled big cross                  </td>  </tr>
 <tr> <td>  11 </td><td>  Open downward triangle         </td> <td style='padding-left:50px;'>  35 </td><td>   Circle with plus                  </td>  </tr>
 <tr> <td>  12 </td><td>  Open rightfacing triangle      </td> <td style='padding-left:50px;'>  36 </td><td>   Circle with X                     </td>  </tr>
 <tr> <td>  13 </td><td>  Open leftfacing triangle       </td> <td style='padding-left:50px;'>  37 </td><td>   Upper half circle                 </td>  </tr>
 <tr> <td>  14 </td><td>  Filled diamond                 </td> <td style='padding-left:50px;'>  38 </td><td>   Filled upper half circle          </td>  </tr>
 <tr> <td>  15 </td><td>  Filled square                  </td> <td style='padding-left:50px;'>  39 </td><td>   Lower half circle                 </td>  </tr>
 <tr> <td>  16 </td><td>  Filled circle                  </td> <td style='padding-left:50px;'>  40 </td><td>   Filled lower half circle          </td>  </tr>
 <tr> <td>  17 </td><td>  Filled upward triangle         </td> <td style='padding-left:50px;'>  41 </td><td>   Left half circle                  </td>  </tr>
 <tr> <td>  18 </td><td>  Filled downward triangle       </td> <td style='padding-left:50px;'>  42 </td><td>   Filled left half circle           </td>  </tr>
 <tr> <td>  19 </td><td>  Filled rightfacing triangl     </td> <td style='padding-left:50px;'>  43 </td><td>   Right half circle                 </td>  </tr>
 <tr> <td>  20 </td><td>  Filled leftfacing triangle     </td> <td style='padding-left:50px;'>  44 </td><td>   Filled right half circle          </td>  </tr>
 <tr> <td>  21 </td><td>  Hourglass                      </td> <td style='padding-left:50px;'>  45 </td><td>   Star                              </td>  </tr>
 <tr> <td>  22 </td><td>  Filled Hourglass               </td> <td style='padding-left:50px;'>  46 </td><td>   Filled star                       </td>  </tr>
 <tr> <td>  23 </td><td>  Bowtie			 </td> <td style='padding-left:50px;'>     </td><td>   				         </td>  </tr>
		   </table>
		   "
		);
// Args
$function[2] = array(
		"[X,] Y [, /ISOTROPIC] [, NSUM=value] [, /POLAR] [, THICK=value] <br> 
		[, /XLOG] [, /YLOG] [, REGION=[ncol,nline,first,last]] [, /INLEGEND] <br>
		[, DESC=string] </p>",
		"[X,] Y [, NSUM=value] [, THICK=value] [, XAXIS={1 | 2}] <br>
		[, YAXIS={1 | 2}] [, /INLEGEND] [, DESC=string]",
		"[, /ISOTROPIC] [, /POLAR] [, REGION=[ncol,nline,first,last]]",
		"[, XAXIS={1,2}] [, YAXIS={1,2}] [, /NEW] [, /DEL]",
		"view1, view2 [, /XAXIS] [, /YAXIS]",
		"[IDX] [, NAME=regex]",
		"[IDX] [, NAME=regex] [, /LAST]",
		"[, REGION=[ncol,nline,first,last]] [X,] [Y] [, /ISOTROPIC] <br>
	         [, NSUM=value] [, /POLAR] [, THICK=value] [, /XLOG] [, /YLOG] <br>
		 [, /INLEGEND] [, DESC=string]",
		"IDX",
		"IDX",
		"",
		"[/HORIZONTAL] [, /VERTICAL] [, /BOX] [, /CLEAR] <br> 
		 [, /DELIMITER] [, /BOTTOM] [, /TOP] [, /LEFT] [, /RIGHT] <br>
		 [, /CENTER] [, /OUT] [, POSITION=[X0,X1,Y0,Y1]] <br>
		 [, /TEXTCOLORS] [, NUMBER=value] [, /VISIBLE] <br>
		 [, CHARSIZE=value]",
		"[, PX=value] [, PY=value] [, TEXT=string] [, COLOR=value] <br>
		 [, CHARSIZE=value] [, CHARTHICK=value] [, ANGLE=value] <br>
		 [, ALIGN=value] [, /NORMAL] [, /DEVICE] [, /VISIBLE] <br>
		 [, XAXIS={1,2}] [, YAXIS={1,2}]",
		"[IDX] [, TEXT=regex] [, /ALL] [, /LAST] [, PX=value] <br>
		 [, PY=value] [, TEXT=string] [, COLOR=value] [, CHARSIZE=value] <br> 
		 [, CHARTHICK=value] [, ANGLE=value] [, ALIGN=value] [, /NORMAL] <br>
		 [, /DEVICE] [, /VISIBLE] [, XAXIS={1,2}] [, YAXIS={1,2}]",
		"[IDX] [, TEXT=regex] [, /ALL] [, /LAST]",
		"[FILE=string] [, /COLOR] [, /A4] [, ENCAPSULATED] [, /J1COL] <br>
		 [, /J2COL] [, /J12CM] [, /PORTRAIT] [, /LANDSCAPE] [, ASPECT=value] <br>
		 [, SCALE=value] [, FONTSIZE=value] [, XSIZE=value] [, YSIZE=value] <br>
	       	 [, /TIMES]",
		"",
		"" 
		);

$function[3] = array(
		"<h4>X</h4>
			<p class='function'>
			A vector representing the abscissa values to be plotted. If X is
			not specified, Y is plotted as a function of point number
			(starting at zero). If both arguments are provided, Y is plotted
			as a function of X.<br>
			This argument is converted to double precision floating-point before plotting.
			Plots created with PLOT are limited to the range and precision of
			double-precision floating-point values.
			</p>
		<h4>Y </h4>
			<p class='function'>
			The ordinate data to be plotted. This argument is
			converted to double-precision floating-point before
			plotting.<br></p>
		<h4>ISOTROPIC</h4>
			<p class='function'>
			Set this keyword to force the scaling of the X and Y
			axes to be equal. <br> </p>
		<h4>NSUM</h4>
			<p class='function'>
			The presence of this keyword indicates the number of
			data points to average when plotting. If NSUM is larger
			than 1, every group of NSUM points is averaged to
			produce one plotted point. If there are m data points,
			then m/NSUM points are displayed. On logarithmic axes a
			geometric average is performed.<br>
			It is convenient to use NSUM when there is an extremely
			large number of data points to plot because it plots
			fewer points, the graph is less cluttered, and it is
			quicker. <br> </p>
		<h4>POLAR</h4>
			<p class='function'>
			Set this keyword to produce polar plots. The X and Y
			vector parameters, both of which must be present, are
			first converted from polar to Cartesian coordinates. The
			first parameter is the radius, and the second is the
			angle (expressed in radians). For example, to make a
			polar plot, you would use a command such as:</p>

			<p class='code'> PLOT, /POLAR, R, THETA </p> 

			<p class='function'>Note: 
			See Using <a
			href='http://127.0.0.1:52017/help/topic/com.rsi.idl.doc.core/AXIS.html#wp1025754'>AXIS
			with Polar Plots</a> for an example that adds axes to a polar plot. 	
			</p>
		<h4>THICK</h4>
		<p class='function'>
			Controls the thickness of the lines connecting the
			points. A thickness of 1.0 is normal, 2 is double wide,
			etc.
		</p>
		<h4>XLOG</h4>
		<p class='function'>
			Set this keyword to specify a logarithmic X axis,
			producing a log-linear plot. Set both XLOG and YLOG to
			produce a log-log plot. Note that logarithmic axes that
			have ranges of less than a decade are not labeled.
		</p>
		<h4>YLOG</h4>
		<p class='function'>
			Set this keyword to specify a logarithmic X axis,
			producing a log-linear plot. Set both XLOG and YLOG to
			produce a log-log plot. Note that logarithmic axes that
			have ranges of less than a decade are not labeled.	
		</p>
		<h4>REGION</h4>
		<p class='function'>
			Set this keyword to specify the region to be used for
			this figure. A region is given by a 4 integer list:
			[ncols,nlines,start,end] where ncols gives the number of
			columns, and nlines the number of lines to consider in
			order to virtually split the device and chose the region
			from the start index to the end index figure in this
			grid. Your are thus able to have multiple figures with
			different sizes.
		</p>
		<h4>INLEGEND</h4>
		<p class='function'>
			Set this keyword to specify if the current curve has to
			be displayed in the legend or not.
		</p>
		<h4>DESC</h4>
		<p class='function'>
			Set this keyword to a string to specify the text to be
			used in the legend to represent the current curve.
			'Curve n' is the default string where n is the curve
			number.
		</p>
		",
		"<h4>X</h4>
		 <p class='function'>
			A vector representing the abscissa values to be plotted.
			If X is not specified, Y is plotted as a function of point
			number (starting at zero). If both arguments are provided, 
			Y is plotted as a function of X. <br>
			This argument is converted to double precision floating-point
			before plotting. Plots created with PLOT are limited to the 
			range and precision of double-precision floating-point values. 
		 </p>
		 <h4>Y</h4>
		 <p class='function'>
			The ordinate data to be plotted. This argument is
			converted to double-precision floating-point before
			plotting.
		 </p>
		 <h4>NSUM</h4>
		 <p class='function'>
		 	The presence of this keyword indicates the number of data 
			points to average when plotting. If NSUM is larger than 1,
			every group of NSUM points is averaged to produce one plotted
			point. If there are m data points, then m/NSUM points are 
			displayed. On logarithmic axes a geometric average is 
			performed. <br>
			It is convenient to use NSUM when there is an extremely 
			large number of data points to plot because it plots fewer 
			points, the graph is less cluttered, and it is quicker.  
		 </p>
		 <h4>THICK</h4>
		 <p class='function'>
		 	Controls the thickness of the lines connecting the points. 
		 	A thickness of 1.0 is normal, 2 is double wide, etc.
		 </p>
		 <h4>XAXIS</h4>
		 <p class='function'>
		 	Set this keyword to define the axis to be used for the plot. 
			1 is default. If no secondary axis defined but keyword set to
			value 2 then it will has no effects and the curve will be 
			plotted using primary axis.
		 </p>
		 <h4>YAXIS</h4>
		 <p class='function'>
		 	Set this keyword to define the axis to be used for the plot. 1
			is default. If no secondary axis defined but keyword set to value
			2 then it will has no effects and the curve will be plotted using 
			primary axis.
		 </p>
		 <h4>INLEGEND</h4>
		 <p class='function'>
		 	Set this keyword to specify if the current curve has to be 
		 	displayed in the legend or not.
		 </p>
		 <h4>DESC</h4>
		 <p class='function'>
			 Set this keyword to a string to specify the text to be used
			 in the legend to represent the current curve. “Curve n” is 
			 the default string where n is the curve number.
		 </p>
		 ",
		 "
		 <h4>ISOTROPIC</h4>
		 <p class='function'>
		 	Set this keyword to force the scaling of the X and Y axes to be equal.
		 </p>
		 <h4>POLAR</h4>
			<p class='function'>
			Set this keyword to produce polar plots. The X and Y
			vector parameters, both of which must be present, are
			first converted from polar to Cartesian coordinates. The
			first parameter is the radius, and the second is the
			angle (expressed in radians). For example, to make a
			polar plot, you would use a command such as:</p>

			<p class='code'> PLOT, /POLAR, R, THETA </p> 

			<p class='function'>Note: 
			See Using <a
			href='http://127.0.0.1:52017/help/topic/com.rsi.idl.doc.core/AXIS.html#wp1025754'>AXIS
			with Polar Plots</a> for an example that adds axes to a polar plot. 	
		 </p>
		 <h4>REGION</h4>
		 <p class='function'>
			Set this keyword to specify the region to be used for this figure. A region
			is given by a 4 integer list: [ncols,nlines,start,end] where ncols gives the
			number of columns, and nlines the number of lines to consider in order to 
			virtually split the device and chose the region from the start index to the
			end index figure in this grid. Your are thus able to have multiple figures
		       	with different sizes.
		 </p>
		 <h4>{XY} RANGE1</h4>
		 <p class='function'>
			Set this keyword to specify the primary axis ranges.
		 </p>
		 <h4>{XY} RANGE2</h4>
		 <p class='function'>
			Set this keyword to specify the secondary axis ranges.
		 </p>
		 ",    	//		"pIMset",         
		 "
		 <h4>{XY}AXIS</h4>
		 <p class='function'>
			Set this keyword to select the axis to affect: 1 for primary 2 for secondary.
		 </p>
		 <h4>NEW</h4>
		 <p class='function'>
			Set this keyword to produce a new axis. If already exists, it will replace the previous one.
		 </p>
		 <h4>DEL</h4>
		 <p class='function'>
			Set this keyword to delete the axis. If the axis is a primary one, the secondary axis will replace it.<br>
			Note: if there is no secondary axis defined and you are trying to delete the primary axis, nothing will happen.
		 </p>
		 <h4>LOG</h4>
		 <p class='function'>
			Set this keyword to specify a logarithmic axis. Note that logarithmic axes that have ranges of less than a decade are not labeled.
		 </p>
		 <h4>ORIENTATION</h4>
		 <p class='function'>
			set to a negative value, it will reverse the axis. This can be done directly when setting range.
		 </p>
		 ",  	//		"pIMsetAxis",
		 "
		 <h4>VIEW{1,2}</h4>
		 <p class='function'>
			Index number of the view you want to link together.
		 </p>
		 <h4>{XY} AXIS
		 </h4>
		 <p class='function'>
			Set this keyword to select the axis to share.<br>
			Note: if there is no secondary axis defined this will delete it. 
			You also can't share axis between 2 figures without side in common 
			and of course you can only share the axis from the common side. 
			Be also sure all figures have the same region dimensions otherwise it
		       	do nothing to avoid strange effects.
		 </p>
		 ",    	//		"pIMShareAxis",
		 "
		 <h4>IDX</h4>
		 <p class='function'>
			Index number of the curve to modify.
		 </p>
		 <h4>NAME</h4>
		 <p class='function'>
			 Set to a regular expression will affect all curves matching the expression.
		 </p>
		 <h4>DESC</h4>
		 <p class='function'>
			 Set this keyword to a string to specify the text to be used
			 in the legend to represent the current curve. “Curve n” is the
			 default string where n is the curve number. <br>
			Set this keyword to select the axis to affect: 1 for primary 2 for secondary.
		 </p>
		 <h4>DISPLAY</h4>
		 <p class='function'>
		 	Set or unset to display or not the curve. This also affect 
		 	the legend but the curve is not deleted but only not displayed.
		 </p>
		 <h4>INLEGEND</h4>
		 <p class='function'>
		 	Set this keyword to specify if the current curve has to be 
		 	displayed in the legend or not.
		 </p>
   		 <h4>NSUM</h4>
		 <p class='function'>
			The presence of this keyword indicates the number of
			data points to average when plotting. If NSUM is larger
			than 1, every group of NSUM points is averaged to
			produce one plotted point. If there are m data points,
			then m/NSUM points are displayed. On logarithmic axes a
			geometric average is performed.<br>
			It is convenient to use NSUM when there is an extremely
			large number of data points to plot because it plots
			fewer points, the graph is less cluttered, and it is
			quicker.
		 </p>
		 </p>
		 <h4>{XY}AXIS</h4>
		 <p class='function'>
			Set this keyword to select the axis to affect: 1 for primary 2 for secondary.
		 </p>
		 ",     //		"pIMsetCurve",
		 "
		 <h4>IDX</h4>
		 <p class='function'>
			Index number of the curve to delete.
		 </p>
		 <h4>NAME</h4>
		 <p class='function'>
			Set to a regular expression will affect all curves matching the expression.
		 </p>
		 <h4>LAST</h4>
		 <p class='function'>
		 	if set and a curve index number “idx” is provided, idx will be understand 
		 	as the index number beginning from the last curve.
		 </p>
		 ",     //		"pIMdelCurve",
		"",  	//		"pIMaddView",
		"
		 <h4>IDX</h4>
		 <p class='function'>
			Index number of the view to delete.
		 </p>
		",  	//		"pIMdelView",
		"
		 <h4>IDX</h4>
		 <p class='function'>
			Index number of the view to select.
		 </p>
		",    	//		"pIMselectView",
		"",    	//		"pIMunselectView",
		"",    	//		"pIMsetLegend",
		"",  	//		"pIMaddNote",
		"",  	//		"pIMsetNote",
		"",  	//		"pIMdelNote",
		"",    	//		"pIM2PS / pIMtoPS",
		"",  	//		"pIMpalette",
		"" 
		);
// Graphics Keywords
$function[4] = array(
		array(0,5,10,20,4,6,8,11,13,14,18,21,29,1,2,7,9,12,14,16,19,22,24,26),
		array(10,19,4,8,11),
		array(0,6,8,11,13,18),    	//		"pIMset",         
		"",  	//		"pIMsetAxis",		
		"",    	//		"pIMShareAxis",	
		"",     //		"pIMsetCurve",   	
		"",     //		"pIMdelCurve",   	
		"",  	//		"pIMaddView",		
		"",  	//		"pIMdelView",		
		"",    	//		"pIMselectView",	
		"",    	//		"pIMunselectView",	
		"",    	//		"pIMsetLegend",		
		"",  	//		"pIMaddNote",		
		"",  	//		"pIMsetNote",		
		"",  	//		"pIMdelNote",		
		"",    	//		"pIM2PS / pIMtoPS",	
		"",  	//		"pIMpalette",		
		""
		);

$gk[0] = array(
	"BACKGROUND",
	"[XY]STYLE",
	"[XY]THICK",
	"CHARSIZE",
	"PSYM",
	"CHARTHICK",
	"SUBTITLE",
	"[XY]TICKFORMAT",
	"SYMSIZE",
	"[XY]TICKINTERVAL",
	"COLOR",
	"T3D",
	"[XY]TICKLAYOUT",
	"THICK",
	"[XY]TICKLEN",
	"DEVICE",
	"[XY]TICKNAME",
	"FONT",
	"TITLE",
	"[XY]TICKS",
	"LINESTYLE",
	"[XY]CHARSIZE",
	"[XY]TICKUNITS",
	"[XY]GRIDSTYLE",
	"[XY]TICKV",
	"[XY]MARGIN",
	"[XY]TITLE",
	"[XY]MINOR",
	"NORMAL",
	"[XY]RANGE");

$gk[1] = array(
	"BACKGROUND=color_hexadecimal_index",
	"{X | Y}STYLE=value",
	"{X | Y}THICK=value",
	"CHARSIZE=value",
	"PSYM=integer{0 to 48}",
	"CHARTHICK=integer",
	"SUBTITLE=string",
	"{X | Y}TICKFORMAT=string",
	"SYMSIZE=value",
	"[XY]TICKINTERVAL=value",
	"COLOR=hexadecimal value",
	"/T3D",
	"[XY]TICKLAYOUT=scalar",
	"THICK=value",
	"[XY]TICKLEN=value",
	"[XY]TICKNAME",
	"FONT=value",
	"TITLE=string",
	"[XY]TICKS=integer",
	"LINESTYLE={0 | 1 | 2 | 3 | 4 | 5}",
	"[XY]CHARSIZE",
	"[XY]TICKUNITS=string",
	"[XY]GRIDSTYLE=integer{0to5}",
	"[XY]TICKV=array",
	"[XY]MARGIN=[left, right]",
	"[XY]TITLE=string",
	"[XY]MINOR=integer",
	"/NORMAL",
	"[XY]RANGE=[min,max]");
$gk[2] = array(
	"http://127.0.0.1:53536/help/topic/com.rsi.idl.doc.core/Graphics_Keywords.html#wp328424",
	"{X | Y}STYLE=value",
	"{X | Y}THICK=value",
	"http://127.0.0.1:53536/help/topic/com.rsi.idl.doc.core/Graphics_Keywords.html#wp266973",
	"PSYM=integer{0 to 48}",
	"http://127.0.0.1:53536/help/topic/com.rsi.idl.doc.core/Graphics_Keywords.html#wp331668",
	"SUBTITLE=string",
	"{X | Y}TICKFORMAT=string",
	"SYMSIZE=value",
	"[XY]TICKINTERVAL=value",
	"http://127.0.0.1:53536/help/topic/com.rsi.idl.doc.core/Graphics_Keywords.html#wp315952",
	"/T3D",
	"[XY]TICKLAYOUT=scalar",
	"THICK=value",
	"[XY]TICKLEN=value",
	"[XY]TICKNAME",
	"FONT=value",
	"TITLE=string",
	"[XY]TICKS=integer",
	"LINESTYLE={0 | 1 | 2 | 3 | 4 | 5}",
	"[XY]CHARSIZE",
	"[XY]TICKUNITS=string",
	"[XY]GRIDSTYLE=integer{0to5}",
	"[XY]TICKV=array",
	"[XY]MARGIN=[left, right]",
	"[XY]TITLE=string",
	"[XY]MINOR=integer",
	"/NORMAL",
	"[XY]RANGE=[min,max]");

$nfunctions = SIZEOF($function[0]);
if(SIZEOF($function[1]) != $nfunctions OR SIZEOF($function[2]) != $nfunctions OR SIZEOF($function[3]) != $nfunctions OR SIZEOF($function[3]) != $nfunctions)
	{die("Function data missing!");}
		
array_multisort($function[0], $function[1], $function[2], $function[3], $function[4]);
/////////////////////////////////////////////////////



// XML PARSER (sounds technical isnt'it?)
// do not forget that tag names are converted into capital letters

function openTag($parser, $tagName, $tagAttributes)
	{
	global $lastTag, $news, $i;
	$lastTag = $tagName;
	if ($lastTag == "NEWS")
		{$i++;}
	if ($lastTag == "DATE")
		{$news[1][$i] = $tagAttributes['VALUE'];}
	}
   
function closeTag($parser, $tagName)
	{
	global $lastTag;
	$lastTag = ""; // really useful?
	}
	
function textValue($parser, $text)
	{
	global $lastTag, $news, $i;
	if ($lastTag == "TITLE")
		{$news[0][$i] .= $text;}
	if ($lastTag == "TEXT")
		{$news[2][$i] .= $text;}
	}


$parserXML = xml_parser_create(); // Create XML parser
xml_set_element_handler($parserXML, "openTag", "closeTag"); // What to do with tags
xml_set_character_data_handler($parserXML, "textValue"); // what to do with text

global $i;
$i = -1;

$feed = "news.xml";
$fp = fopen($feed, "r");
if (!$fp) die("XML file not found");

while ($line = fgets($fp, 1024))
	{
	//echo htmlentities($line)."<br><br>";
	xml_parse($parserXML, $line, feof($fp)) or die("XML error");
	}

$nnews = SIZEOF($news[0]);
array_multisort($news[1], SORT_DESC, $news[0], $news[2]);
?>

<p class="menu"><a class="menu" href="index.php">Home</a></p>

<p style="text-align:left">Latest Version: <?php echo date('d/m/Y' , filemtime($pimfile)) ?><br />
<a class="menu" href="<?php echo $pimfile; ?>">Download</a></p>

<p class="menu"><span style="font-variant: small-caps; font-size: 12pt">Online Help</span><br />
<a class="menu" href="help.php">All functions</a></p>

<form action="results.php" method="post" style="margin-top: 0px; margin-bottom: 4px;">Search: <input type="text" name="search" size=15 /></form>

<p><span style="font-variant: small-caps; font-size: 12pt">Latest News</span><br />
<?php
if ($nnews < $nlast_news)
	{$nlast_news = $nnews;}
for($i = 0 ; $i < $nlast_news ; $i++)
	{
	if (strlen($news[0][$i]) > $short_news_title_length)
		{
		$short_title = substr($news[0][$i], 0, $short_news_title_length); // select the right nb of char from 0
		$tmp = strrpos($short_title, " ");
		$short_title = substr($short_title, 0, $tmp);
		$tmp_end = "...";
		}
	else
		{
		$short_title = $news[0][$i];
		$tmp_end = "";
		}

	echo '<a class="menu" href="news.php?news_id='.$i.'">'.$short_title.$tmp_end.'</a><br/>'; // display up to the last space
	}
?>
<a class="memu" href="news.php" style="font-style: italic;">more...</a>
</p>

<p><span style="font-variant: small-caps; font-size: 12pt">Screenshots</span><br />
<a class="menu" href="photos.php" style="font-style: italic;">more...</a></p>

</div>
<!-- end of the left panel-->

<!-- begining of the main panel (margin must be at least the width of the left panel) -->
<div style="width: 600px; margin-left: 300px; padding-left: 10px;">
<!-- this div will be closed in the _botom.php -->
