// jQuery team recommandations: http://docs.jquery.com/JQuery_Core_Style_Guidelines

var nVertex = 3,
    catalogs,
    catName2cat = {};

/* For SAMP */
var meta = {
    "samp.name": "QueryCatResult",
    "samp.description": "QueryCat result",
    "samp.icon.url": "http://" + document.location.hostname + ":8877/content/mydb.png"
};
var sampConnector;
var sampStatusId;
var sampCc;
var sampCallHandler;


function nVertexes(n) {
  "use strict";
  var diff, i;
  if (n > 2 && n < 11) {
    diff = n - nVertex;
    if (diff > 0) {
      // console.log("Add " + diff + " vertex. nVertex = " + nVertex + " ; n = " + n)
      var html = '';
      for (i = nVertex; i < n; i++) {
        html += '<li class="radioOptions" id="vertex' + i + '"><label for="optionVertexes' + i + '"> Vertex ' + i + ': </label>\n<input type="text" id="optionVertexes' + i + '" placeholder="00 00 00 +00 00 00" ></input></li>';
      }
      $( "#vertexList" ).append(html);
    } else { 
      // console.log("Rm " + (-diff) + " vertex. nVertex = " + nVertex + " ; n = " + n)
      for (i = nVertex - 1; i >= n; i--) {
        $( "#vertex" + i ).remove();
      }
    }
    nVertex = n;
  }
}

function format(n){
  "use strict";
  var s = new String(n);
  if (n < 1000){
     return n;
  } else {
     var to = s.length - 3; //, to = s.length;
     while (to > 0) {
          s = s.substr(0, to) + "," + s.substr(to);
          to -= 3;
     }
  }
  return s;
}
/*function initVertexes() {
    "use strict";
    var i, html = '';
    for (i = 0; i < nVertex; i++) {
  html += '<li class="radioOptions" id="vertex' + i + '"><label for="optionVertexes"> Vertex ' + i + ': </label><input type="text" id="optionVertexes" placeholder="00 00 00 +00 00 00" ></input></li>';
    }
    $( "#vertexList" ).append(html);
}*/

$(function() { /* Exec only when page is loaded! */
    "use strict";
    /*var chosenCat = "2MASS";
    myobj[chosenCat];
    var myFunc = function (param1, param2) {

    };*/

    function autocomp(catList) {
        "use strict";
        $( "#catName" ).autocomplete({
            autoFocus: true,
            delay: 0,     // time in ms before activating the autocomplete
            minLength: 0, // number of caracters before activating the autocomplete
            source: catList,
            close: function(event, ui) {
                "use strict";
                var catName = $('#catName').val();
                var imgUrl = "";
                if (!catName2cat[catName]) {
                    $('#catId').html("");
                    $('#catDesc').html("");
                    $('#nRows').html("");
                    $('#imgDensMap"').attr('src', "");
                    $('#imgDensMapRef').attr('href', "");
                    $('#imgDensMap').attr('title', "Density map not available");
                } else {
                    /* Vizier part */
		     if (catName2cat[catName].vizTab.match("^Not")) {
                        $('#catId').html(catName2cat[catName].vizTab);
                        imgUrl = "http://alasky.u-strasbg.fr/footprints/tables/vizier/" + catName2cat[catName].id.replace(/\//g,"_") + "/densityMap?format=png&size=normal";
                    } else {
                        $('#catId').html("<a href='http://vizier.u-strasbg.fr/viz-bin/VizieR-3?-source=" + catName2cat[catName].vizTab + "' target='_blank'>" + catName2cat[catName].vizTab + "</a>");
                        imgUrl = "http://alasky.u-strasbg.fr/footprints/tables/vizier/" + catName2cat[catName].vizTab.replace(/\//g,"_") + "/densityMap?format=png&size=normal";
                    }
                    $('#catId').html("<b>" + catName2cat[catName].id + "</b>");
                    $('#catDesc').html("<b>" + catName2cat[catName].desc + "</b>");
                    $('#nRows').html(format(catName2cat[catName].nRows));
  		    //console.log('MF ok' + format(catName2cat[catName].nRows) + $('#nRows').html(catName2cat[catName].nRows) );
                    $('#imgDensMap').attr('src', imgUrl);
                    $('#imgDensMapRef').attr('href', imgUrl);
                    //$('#imgDensMap').attr('title', "Density map of catalog " + catName2cat[catName].id);

                    fillMetaTab(catName2cat[catName].id);
                }
            }
        });
    };

//     $('#catName')[0].onkeypress =  function() {
//         "use strict";
//         var catName = $(this).val();
//         if (!catName2cat[catName]) {
//             $('#catVizId').html("Undefined!");
//         } else {
//             $('#catVizId').html(catName2cat[catName].vizTab);
//             fillMetaTab(catName2cat[catName].id);
//         }
//     };

    $.getJSON("cats/cats.json", function(data) {
        "use strict";
        var availableCats = [];
        catalogs = data.cats;
        $.each(catalogs, function(key, val) {
            availableCats.push(val.name);
            // catName2cat.setAttribute(val.name, val);
            catName2cat[val.name] = val;
        });
        autocomp(availableCats);
    });

    /*$('#optionNVertex')[0].oninput = function() {
  "use strict";
  // console.log('valeur: ' + $(this).val());
  nVertexes(parseInt($(this).val()));
    };

    $('#optionNVertex')[0].onchange = function() {
  "use strict";
  // console.log('valeur: ' + $(this).val());
  nVertexes(parseInt($(this).val()));
    };*/

   /* $('#optionHealpixNside')[0].onchange = function() {
        "use strict";
        var nside = parseInt($(this).val());
        // $('#optionConeSearchRadius')[0].max = 12 * nside * nside;
        $('#optionHealpixIdx').attr("max", (12 * nside * nside) - 1)
    };*/

    $('#distUnitSelect')[0].onchange = function() {
        "use strict";
        var unit = $(this).val();
        if (unit == "mas") {
            $('#optionConeSearchRadius').attr("max", 60000); // => 1arcmin
        // $('#optionConeSearchRadius').attr("step", 1); // => 1 mas
        } else if (unit == "arcsec") {
            $('#optionConeSearchRadius').attr("max", 3600); // => 1 deg
        // $('#optionConeSearchRadius').attr("step", 0.1); // => 100 mas
        } else if (unit == "arcmin") {
            $('#optionConeSearchRadius').attr("max", 600); // => 10 deg
        // $('#optionConeSearchRadius').attr("step", 0.01); // => 100 mas
        } else if (unit == "deg") {
            $('#optionConeSearchRadius').attr("max", 60); // => 60 deg
        }
    };

    $('#boxWidthUnitSelect')[0].onchange = function() {
        "use strict";
        var unit = $(this).val();
        if (unit == "mas") {
            $('#optionConeSearchRadius').attr("max", 60000); // => 1arcmin
        // $('#optionConeSearchRadius').attr("step", 1); // => 1 mas
        } else if (unit == "arcsec") {
            $('#optionConeSearchRadius').attr("max", 3600); // => 1 deg
        // $('#optionConeSearchRadius').attr("step", 0.1); // => 100 mas
        } else if (unit == "arcmin") {
            $('#optionConeSearchRadius').attr("max", 600); // => 10 deg
        // $('#optionConeSearchRadius').attr("step", 0.01); // => 100 mas
        } else if (unit == "deg") {
            $('#optionConeSearchRadius').attr("max", 60); // => 60 deg
        }
    };
   
    $('#boxHeightUnitSelect')[0].onchange = function() {
        "use strict";
        var unit = $(this).val();
        if (unit == "mas") {
            $('#optionConeSearchRadius').attr("max", 60000); // => 1arcmin
        // $('#optionConeSearchRadius').attr("step", 1); // => 1 mas
        } else if (unit == "arcsec") {
            $('#optionConeSearchRadius').attr("max", 3600); // => 1 deg
        // $('#optionConeSearchRadius').attr("step", 0.1); // => 100 mas
        } else if (unit == "arcmin") {
            $('#optionConeSearchRadius').attr("max", 600); // => 10 deg
        // $('#optionConeSearchRadius').attr("step", 0.01); // => 100 mas
        } else if (unit == "deg") {
            $('#optionConeSearchRadius').attr("max", 60); // => 60 deg
        }
    };


    /*function addMetaTab(){
        "use strict";
  var html = ''; 
        if (!$('#tabMeta')[0]) {
      html += '<div id="tabMeta">';
      html += '<table cellpadding="0" cellspacing="0" border="0" class="display" id="tab_meta">';
      html += '<thead><tr></th><th width="20%">ColName</th><th width="15%">DataType</th><th width="15%">Format</th><th width="20%">Unit</th><th width="20%">UCD</th></tr></thead>';
      html += '<tbody></tbody>';
      html += '</table>';
      html += '</div>';
      $('#catFieldSet').append(html);
  } // <th width="10%"><input type="checkbox" id="selectall" />
    }
    
    function rmMetaTab(){
        if ($('#tabMeta')[0]) {
      $('#tabMeta').remove();
  }
    }*/
    
    // $("#dialog").dialog();
    
    $('#tabMetaToggleDiv').hide();
    $('#plotToggleDiv').hide();
    $('#infoToggleDiv').hide();
    $('#imgConnSAMP').hide();
    
    // Pour faire plus jolie, voir p. 141 de "jQuery in action"
    $('#PlotCaption img:first').click(function() {
        $('#plotToggleDiv').toggle('slow');
        return false;
    });


    $('#plotform').submit( function() {
	console.log('Toto');
        "use strict";
        var url = '/Plot?';
	url += 'func=' + $('#plotFuncSelect').val();
	url += '&xval=' + $('#xPlotVal').val();
	url += '&yval=' + $('#yPlotVal').val();
        //if ($('#radioOutputPLOT').attr('checked')  == 'checked') {
	//}
	return url;
    });

    // Pour faire plus jolie, voir p. 141 de "jQuery in action"
    $('#tabMetaCaption img:first').click(function() {
        $('#tabMetaToggleDiv').toggle('slow');
        return false;
    });
     $('#infoCaption img:first').click(function() {
        $('#infoToggleDiv').toggle('slow');
        return false;
    });
//   $('#tabMeta a:first').click(function() {
//     $('#tabMetaToggleDiv').toggle();
//     return false;
//   });
    
    function fillMetaTab(catName) {
        "use strict";
        var metaUrl = 'QueryCat?getMeta&catName=' + catName;
        //console.log("catName: " + catName);
        // addMetaTab();
        $('#tab_meta').dataTable( {
            // "sScrollX": "100%",
            "bDestroy": true,
            "bAutoWidth": false,
            "bProcessing": false,
            "bPaginate": false,
            "bLengthChange": false,
            "bSort": false,
            "bFilter": false,
            "bInfo": false,
            "bDeferRender": false,
            "sAjaxSource": metaUrl,
            "fnServerData": function (sSource, aoData, fnCallback) {
                /* Add some data to send to the source, and send as 'POST' */
                // aoData.push( { "name": "my_field", "value": "my_value" } );
                $.ajax( {
                    "dataType": 'json',
                    "type": "GET",
                    "url": sSource,
                    "success": function (json) {
                        var aData = json;
                        $(aData.aaData).each(function () {
                            this.unshift("<input type=\"checkbox\" name=\"catMetaCheckBox\" value=\"" + this[0] + "\" checked = \"checked\" />");
                        });
                        fnCallback(aData);
                        activateCheckbox();
                    },
                    "error": function (xhr, error, thrown) {
                        if ( error == "parsererror" ) {
                            alert("DataTables warning: JSON data from server could not be parsed. "+
                                  "This is caused by a JSON formatting error." );
                        } else {
                            alert("Error type: " + error + ". Caused by:" + thrown);
                        }
                    },
                    "statusCode": {
                        400: function(xhr, error, thrown) {
                            $('#errorDialog').remove();
                            $('#catFieldSet').append('<div id="errorDialog" title="Error">' + xhr.responseText + '</div>');
                            $('#errorDialog').dialog({ modal: true, buttons: { "Ok": function() { $(this).dialog("close"); } } });
                        }
                    }
                });
            }
        });
    };
    
    $('#allMetaCheckbox').click(function() {
        "use strict";
        var all = $('#tab_meta tbody :checkbox');
        if (!this.checked) { // => all selected //  && all.length == checked.length
            $(all).each(function () {
                this.checked = false;
            });
        } else if (this.checked && all.length != $('#tab_meta tbody :checkbox:checked').length) { // => not all selected
            $(all).each(function () {
                this.checked = true;
            });
        }
    });

    function activateCheckbox() {
        "use strict";
        $('#tab_meta tbody :checkbox').click(function() {
            "use strict";
            var globCheckbox=$('#allMetaCheckbox');
            if (!this.checked && globCheckbox.attr('checked') == 'checked') { // => al least on non selected
                globCheckbox.removeAttr('checked');
            } else if (this.checked && globCheckbox.attr('checked') == undefined) {
                if ($('#tab_meta tbody :checkbox').length == $('#tab_meta tbody :checkbox:checked').length) { // => all selected
                    globCheckbox.attr('checked', 'checked');
                }
            }
        });
    };

    $('#buttonSAMP').click(function() {
        "use strict";
    if (sampConnector) {
        clearInterval(sampStatusId);
        if (sampConnector.connection) {
            sampConnector.unregister();
        }
        sampConnector = null;
        $('#imgConnSAMP').hide();
        $('#imgDiscSAMP').show();
    } else {
        sampCc = new samp.ClientTracker();
        sampCallHandler = sampCc.callHandler;
            sampConnector = new samp.Connector("QueryCat result", meta, sampCc, sampCc.calculateSubscriptions());
            sampConnector.register();
        if (sampConnector) {
              sampStatusId = setInterval(function() {
              if (sampConnector.connection) {
                  $('#imgConnSAMP').show();
                  $('#imgDiscSAMP').hide();
          }
          }, 1000);
        }
        }
        // on ne soumet pas le FORMulaire
        return false;
    });

    function buildUrl() {
        "use strict";
        var colList = "";
        var first = true;
        var url =  'QueryCat?catName=' + catName2cat[$('#catName').val()].id;
        //var url =  'QueryCat?catName=' + $('#catId').val();
        var colTab = $('#tab_meta tbody :checkbox:checked');
        // Columns
        if (colTab.length != $('#tab_meta tbody :checkbox').length) { // by default, all columns
            $(colTab).each(function () {
                if (first) {
                    first = false;
                } else {
                    colList += ",";
                }
                colList += this.value;
            });
            if (colList == "") {
                $('#infoDialog').remove();
                $('#catFieldSet').append('<div id="infoDialog" title="Error">At least one column must be selected, if not, all columns are returned!</div>');
                $('#infoDialog').dialog({ modal: true, buttons: { 'Ok': function() { $(this).dialog('close'); } } });
            } else {
                url += '&col=' + colList;
            }
        }
        // Sky Area      
        if ($('#radioAllSky').attr('checked') == 'checked') {
            url += '&mode=allsky';
        } else if ($('#radioConeSearch').attr('checked') == 'checked') {
            url += '&mode=cone';
            url += '&pos=' + encodeURIComponent($('#optionConeSearchCenter').val());
            url += '&r=' + $('#optionConeSearchRadius').val() + $('#distUnitSelect').val();
        } else if ($('#radioHealpixIdx').attr('checked') == 'checked') {
            url += '&mode=healpix';
            url += '&nside=' + $('#optionHealpixNside').val();
            url += '&ipix=' + $('#optionHealpixIdx').val();
        } else if ($('#radioBox').attr('checked') == 'checked') {
        url += '&mode=box';
        url += '&pos=' + encodeURIComponent($('#optionBoxCenter').val());
        url += '&width=' + $('#optionBoxWidth').val() + $('#boxWidthUnitSelect').val();
        url += '&height=' + $('#optionBoxHeight').val() + $('#boxHeightUnitSelect').val();
        if ($('#optionBoxPA').val() != undefined && $('#optionBoxPA').val() != '' && $('#optionBoxPA').val() != '0') {
            url += '&angle=' + $('#optionBoxPA').val() + $('#boxPAUnitSelect').val();
        }
    } else if ($('#radioZone').attr('checked') == 'checked') {
            url += '&mode=zone';
            url += '&minRA=' + $('#optionZoneRaMin').val();
            url += '&maxRA=' + $('#optionZoneRaMax').val();
            url += '&minDec=' + $('#optionZoneDecMin').val();
            url += '&maxDec=' + $('#optionZoneDecMax').val();
    }
        // Ouput format
        if ($('#radioOutputWeb').attr('checked') == 'checked') {
            url += '&format=jsondt';
        } else if ($('#radioOutputSAMP').attr('checked') == 'checked') {
        url += '&format=votable';
    } else if ($('#radioOutputTSV').attr('checked') == 'checked') {
            url += '&format=tsv';
        } else if ($('#radioOutputCSV').attr('checked') == 'checked') {
            url += '&format=csv';
        } else if ($('#radioOutputPSV').attr('checked') == 'checked') {
            url += '&format=psv';
        } else if ($('#radioOutputSSV').attr('checked') == 'checked') {
            url += '&format=ssv';
        } else if ($('#radioOutputFITS').attr('checked') == 'checked') {
            url += '&format=fits';
        } else if ($('#radioOutputJSON').attr('checked') == 'checked') {
            url += '&format=json';
        } else if ($('#radioOutputVOT').attr('checked') == 'checked') {
            url += '&format=votable';
        } else if ($('#radioOutputPLOT').attr('checked') == 'checked') {
            url += '&format=plot';
        }
    // Condition
    if ($('#optionFilter').val() != undefined && $('#optionFilter').val() != '') {
        url += '&filter=' + encodeURIComponent($('#optionFilter').val());
    }
    // Output limit
    if ($("#radioLimit").attr("checked") == "checked") {
        url += '&limit=' + $('#outputLimitN').val();
    }
        return url;
    };
   
    /* Detect than we close the web page
       $(window).bind('unload', function(){connector.unregister();}); */


    $('#catfileform').submit(function() {
        "use strict";
        var url = buildUrl();
        if ($('#radioOutputWeb').attr('checked')  == 'checked') {
            fillDataTab(url);
        } else if ($('#radioOutputSAMP').attr('checked') == 'checked') {
            rmTabData();
            if (sampConnector && sampConnector.connection) {
                var tableId = url;
                var tableName = $('#catName').val();
                var loc = window.location.href;
                url = loc.substring(0, loc.lastIndexOf('/')) + '/' + url;
                var msg = new samp.Message("table.load.fits", {"table-id": tableId, "url": url, "name": tableName});
                sampConnector.connection.notifyAll([msg]);
                $('#dataUrl').html(url);
            } else {
                $('#infoDialog').remove();
                $('#catFieldSet').append('<div id="infoDialog" title="Error">Your are not connected to a SAMP hub!<br/>Click the icon to try to connect a SAMP hub.</div>');
                $('#infoDialog').dialog({ modal: true, buttons: { 'Ok': function() { $(this).dialog('close'); } } });
            }
        } else {
            $('#dataUrl').html("http://" + document.location.hostname + "/QueryCat/" + url);
            rmTabData();
            window.location = url;
        }
        return false;
    });

    function rmTabData(){
        "use strict";
        if ($('#tabData')[0]) {
            $('#tabData').remove();
        }
    }

    function createTabData(metadata){
        "use strict";
        // remove tab_data if exists
        rmTabData();
        // create tab_data
        var html = '<div id="tabData"style="overflow-x: auto ; width: 880px">';
        html += '<table cellpadding="0" cellspacing="0" border="0" class="display" id="tab_data">'; 
        html += '<thead><tr>';
        $(metadata).each(function () {
            html += '<th>';
            html += this.name;
            html += '</th>'
        });
        html += '</tr></thead><tbody></tbody></table></div>';
        $('#queryResultFieldSet').append(html);
    }

    $('#progressbar').hide();

    function fillDataTab(dataUrl) {
        "use strict";
	//$('#dataUrl').html("http://" + document.location.hostname + "/QueryCat/" + dataUrl);
        $('#dataUrl').html("http://" + document.location.host + "/" + dataUrl);
        //console.log("dataUrl = " + dataUrl);
        $('#progressbar').show();
        rmTabData();
        $.ajax({
            "dataType": 'json',
            "type": "GET",
            // "async": false,
            "url": dataUrl,
            //"url": '/cats/fx.json',
            "success": function (json) {
                "use strict";
                createTabData(json.columnmeta);
                $('#tab_data').dataTable( {
                    "bDestroy": true,
                    "bProcessing": true,
                    "iDisplayLength": 25,
                    "aLengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
                    "bPaginate": true,
                    "bLengthChange": true,
                    "bDeferRender": true,
                    "aaData": json.data
                    // "sAjaxDataProp": "data",
                });
                $('#progressbar').hide();
            },
            "error": function (xhr, error, thrown) {
                $('#errorDialog').remove();
                $('#queryResultFieldSet').append('<div id="errorDialog" title="Error">' + xhr.responseText + '</div>');
                $('#errorDialog').dialog({ modal: true, closeOnEscape: false, buttons: { "Ok": function() { $(this).dialog("close"); } } });
                $('#progressbar').hide();
            }
        });

    };

    function disableConeSearch() {
        "use strict";
        $("#optionConeSearch label, #optionConeSearch input, #optionConeSearch select").attr("disabled", "disabled");
    };
    function disableHealpixIdx() {
        "use strict";
        $("#optionHealpixCell label, #optionHealpixCell input, #optionHealpixCell select").attr("disabled", "disabled");
    };
    function disableBox() {
        "use strict";
        $("#optionBox label, #optionBox input, #optionBox select").attr("disabled", "disabled");
    };
    function disableZone() {
        "use strict";
        $("#optionZone label, #optionZone input, #optionZone select").attr("disabled", "disabled");
    };
    function disablePolygon() {
        "use strict";
        $("#optionPolygon label, #optionPolygon input, #optionPolygon select").attr("disabled", "disabled");
    };

    function enableConeSearch() {
        "use strict";
        $("#optionConeSearch label, #optionConeSearch input, #optionConeSearch select").removeAttr("disabled");
    };
    function enableHealpixIdx() {
        "use strict";
        $("#optionHealpixCell label, #optionHealpixCell input, #optionHealpixCell select").removeAttr("disabled");
    };
    function enableBox() {
        "use strict";
        $("#optionBox label, #optionBox input, #optionBox select").removeAttr("disabled");
    };
    function enableZone() {
        "use strict";
        $("#optionZone label, #optionZone input, #optionZone select").removeAttr("disabled");
    };
    function enablePolygon() {
        "use strict";
        $("#optionPolygon label, #optionPolygon input, #optionPolygon select").removeAttr("disabled");
    };


    function disableLimit() {
        "use strict";
    $("#outputLimitN").attr("disabled", "disabled");
    }
    function enableLimit() {
        "use strict";
        $("#outputLimitN").removeAttr("disabled");
    }

    // initVertexes();
    disableConeSearch();
    disableHealpixIdx();
    disableBox();
    disableZone();
    disablePolygon();

    //disableLimit();

    $( "#skyareaFieldSet input[name='skyAreaRadio']" ).change(function() {
        "use strict";
        if ( $("#radioAllSky").attr("checked") == "checked") {
            disableConeSearch();
            disableHealpixIdx();
        disableBox();
        disableZone();
            disablePolygon();
        } else if ($( "#radioConeSearch").attr("checked")  == "checked") {
            enableConeSearch();
        disableBox();
        disableZone();
            disableHealpixIdx();
            disablePolygon();
        } else if ($( "#radioHealpixIdx").attr("checked") == "checked") {
            disableConeSearch();
            enableHealpixIdx();
        disableBox();
        disableZone();
            disablePolygon();
    } else if ($("#radioBox").attr("checked") == "checked") {
        disableConeSearch();
            disableHealpixIdx();
        enableBox();
        disableZone();
            disablePolygon();
    } else if ($("#radioZone").attr("checked") == "checked") {
            disableConeSearch();
            disableHealpixIdx();
        disableBox();
        enableZone();
            disablePolygon();
        } else if ($( "#radioPolygon" ).attr("checked") == "checked") {
            disableConeSearch();
            disableHealpixIdx();
        disableBox();
        disableZone();
            enablePolygon();
        } else {
            alert("No radio bouton checked!");
        }
    });

    $("#outputFieldSet input[name='limitRadio']").change(function() {
        "use strict";
    if ($("#radioLimit").attr("checked") == "checked") {
        enableLimit();
    } else if ($("#radioNoLimit").attr("checked") == "checked") {
        disableLimit();
    }
    });

    $('#catName').focus();

});

//$(document).ready(function() {
//$(".toto").css("border","3px solid red");
//$( ".toto" ).css('background-color', 'red');
//});
// $(function() {
//      $( "#radio" ).buttonset();
// });
