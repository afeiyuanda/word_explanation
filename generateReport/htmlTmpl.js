/*   用户给html制作提供模板,
 
 
 */
var rf = require("fs");
var util = require("./util");
var parseXml = require('./parseXml.js');
var REPORT_HTML_RAW_DATA = "http://img.biocloud.cn/cloud_beta_1.0/v_1.3/Raw_data1.png";

exports.addBodyHeadString = function(concfgtestObj) {
	var headStr =
		"<input id=\"app_report_html\" type=\"hidden\" version=\"1.1\" />\n" +
		"<input type='hidden' value='createByNodejs'>" +
		/*"<!DOCTYPE html>" +
"<html lang=\"en\">\n"+*/
"<head>\n"+
"<meta charset=\"UTF-8\">\n"+
"<title>Document</title>\n"+
"<link href=\"http://cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css\" rel=\"stylesheet\">\n"+
"<link href=\"http://cdn.bootcss.com/font-awesome/4.5.0/css/font-awesome.min.css\" rel=\"stylesheet\">\n"+
/*
"<link href=\"http://www-dev.bmk.local/js/reportHtml/reportHtml.css\" rel=\"stylesheet\">\n"+
*/
/*"<link href=\"static/select2.min.css\" rel=\"stylesheet\">\n"+
"<link href=\"static/reportHtml.css\" rel=\"stylesheet\">\n"+
"<link rel=\"stylesheet\" href=\"/static/css/css/raxus.css\">\n"+
"<link href=\"static/raxus.css\" rel=\"stylesheet\">\n"+
"<link href=\"static/report_final.css\" rel=\"stylesheet\">\n"+*/

"<link href=\"/static/css/css/raxus.css\" rel=\"stylesheet\">" +
"<link href=\"/static/css/css/plugins/select2/select2.min.css\" rel=\"stylesheet\">" +
"<link href=\"/static/css/css_new/css/report_html/reporthtml.css\" rel=\"stylesheet\">"+
"</head>\n"+
"<body>";
		return headStr + 
		/*"<div class='wrapper wrapper-content article tab-pane active'>"+
		"<div class='row'>"+
          "<div class='col-lg-10 col-lg-offset-1'>"+
              "<div class='ibox'>"+
                 "<div class='ibox-content' id='reportblack' >"+*/

			"<div class=\"report-box jq-hate-too\" id=\"app_report_html_main\">" +
			"<div class=\"box-left\">\n" +
			"<h4 class=\"final-title\">" + concfgtestObj.report_name + "</h4>\n" +
			"<p class=\"final-title-p\">项目编码:" + concfgtestObj.report_code +
			"   |    项目完成时间:" + concfgtestObj.report_time + "</p>\n" +
			"<div class=\"final-digest\"> \n" +
			"<h5 id=\"digest\" class=\"final-m-title\">摘要 </h5>" +
			"<div class=\"showOrHide\">" + concfgtestObj.report_abstract +
			"</div>" +
			"</div>";
	}
/*
	//转换对象成html, 判断方法
exports.parseObject = function(object, fileArray) {
	for (var item in object) {
		if (item != '$' && object[item] == 'file') {
			html += parseFile(object.$, fileArray);
			type = 'file';
		} else if (item != '$' && object[item] == 'file_list') {
			html += parseFileList(object, fileArray,);
			type = 'file_list';
		} else if (item != '$' && object[item] == 'pic') {
			html += parsePic(object.$, fileArray, firstImage);
			type = 'pic'
		} else if (item != '$' && object[item] == 'h1') {
			if (firsttitle) {
				html += '</div>';
			}
			html += "<div class=\"acdsee-comment_H1_" + H1num + "\"><h5 id=\"acdsee-comment_H1_" + H1num + "\" class=\"final-m-title\">" + object.$.desc + " </h5>";
			type = 'h1';
			firsttitle = 'no';
			H1num++;
		} else if (item != '$' && object[item] == 'h2') {
			html += "<p id=\"acdsee-comment_H2_" + H2num + "\" class=\"final-title-bold\">" + object.$.desc + "</p>";
			type = 'h2';
			H2num++;
		} else if (item != '$' && object[item] == 'h3') {
			
			//html += "<p id=\"acdsee-comment_H3_" + H2num + "\" class=\"final-title-three\">" + object.$.desc + "</p>";
			html += "<p id=\"acdsee-comment_H3_" + H3num + "\" name=\"H2_" + (H2num-1) + "\" class=\"final-title-three\">"
				+ object.$.desc + "</p>";
			console.log("<p id=\"acdsee-comment_H3_" + H3num + "\" name=\"H2_" + (H2num-1) + "\" class=\"final-title-three\">"
				+ object.$.desc + "</p>");
			type = 'h3';
		} else if (item != '$' && object[item] == 'p') {
			html += "<p class=\"final-p\">" + object.$.desc + "</p>";
			type = 'p';
		} else if (item != '$' && object[item] == 'pic_list') {
			html += parsePicList(object, fileArray, firstImage, WheelImage);
			type = 'pic_list';
		} else if (item != '$' && object[item] == 'ref_list') {
			html += parseRefList(object, fileArray);
			type = 'ref_list';
		} else if (item != '$' && object[item] == 'table') {
			html += parseTbale(object.$, fileArray);
			type = 'table';
		}
		if (item == 'h1' && !'图片预览'.test(object.$.name)) {
			h2number++;
		}
		if (item == 'h2') {
			h2number++;
		}

	}
	return html;
}*/

exports.parseFile = function(file, fileArray) {
	util.replaceFilePath(file, fileArray);
	return "<div class=\"other-padding\">" +
		"<div class=\"acdsee-comment-img\">\n" +
		"<img class=\"jq-img\" fileType=\"" + file.type + "\" fileName=\"" + file.name + "\" " +
		"src=\"" + REPORT_HTML_RAW_DATA + "\" fileAnno=\"" + file.desc + "\" path=\"" + file.path + "\">\n" +
		"\t\t\t\t<div class=\"acdsee-comment-word-one\">\n" +
		"\t\t\t\t\t<p class=\"img-comment-word\">" + file.name + "</p>\n" +
		"\t\t\t\t\t\t\t<p class=\"img-comment-p\">" + file.desc + "</p>\n" +
		"\t\t\t\t</div>\n" +
		"\t\t</div>" +
		"\t</div>\n";
}

exports.parseFileList = function(files, fileArray,WheelTable) {
	if(!files.$$){
		return "";
	}
	var html = "<div class=\"other-padding\"><div class=\"final-carousel\">";
	if (files.$$.length > 1) {
		html += "\t\t<i class=\"fa fa-angle-left jq-left\"></i>";
	}
	html += "\t\t<div class=\"in-box\" id=\"wheel_table"+WheelTable+"\">";
	var descFileList = files.$.desc;
	var fileList = files.$$;
	for (var i in fileList) {
		var file = fileList[i].$;
		var type = fileList[i].path;
		util.replaceFilePath(file, fileArray);
		if (i == 0) {

			html += "\t\t\t<div class=\"wheel is-it\" title=\"Image from Unsplash\" data-gallery=\"\"" +
				" fileAnno=\"" + file.desc + "\" fileType=\"" + file.type + "\" path=\"" + file.path + "\" fileName=\"" + file.name + "\">";
		} else {
			html += "\t\t\t<div class=\"wheel\" title=\"Image from Unsplash\" data-gallery=\"\"" +
				" fileAnno=\"" + file.desc + "\" fileType=\"" + file.type + "\" path=\"" + file.path + "\" fileName=\"" + file.name + "\">";
		}
		if (/^.*\.KEGG\.list$/g.test(file.path) || /^.*\.html/g.test(file.path)) {

			var copyFilePath = ( file.path);
			if (!(file.path.endsWith(".cloud"))) {
				copyFilePath = file.path + ".cloud";
			}
			var flag = parseXml.ifFileExit(copyFilePath);
			if (flag) {
				html += "<img class=\"\" copyFilePath=\"" + copyFilePath + "\" onclick=\"getKEGGHtml(this);\" src=\"https://img.biocloud.net/AppImg/3.1/de novo RNA-seq/report/Raw_data1.png\">" +
					"<div class=\"carousel-word\">" +
					"<p class=\"carousel-word-title\">" + file.name + "</p>" +
					"<p class=\"carousel-word-p\">" + descFileList + "</p>" +
					"</div>" +
					"\t\t\t</div>";
			} else {
				html += "<img onclick=\"getKEGGHtmlError();\" src=\"https://img.biocloud.net/AppImg/3.1/de novo RNA-seq/report/Raw_data1.png\">" +
					"<div class=\"carousel-word\">" +
					"<p class=\"carousel-word-title\">" + file.name + "</p>" +
					"<p class=\"carousel-word-p\">" + descFileList + "</p>" +
					"</div>" +
					"\t\t\t</div>";
			}
		} else {
			html += "<img class=\"jq-carousel\" name='" + file.type + "' src=\"https://img.biocloud.net/AppImg/3.1/de novo RNA-seq/report/Raw_data1.png\">" +
				"<div class=\"carousel-word\">" +
				"<p class=\"carousel-word-title\" >" + file.name + "</p>" +
				"<p class=\"carousel-word-p\">" + descFileList + "</p>" +
				"</div>" +
				"\t\t\t</div>";
		}
	}
	html += "\t\t\t<div id=\"blueimp-gallery\" class=\"blueimp-gallery\">" +
		"\t\t\t\t\t<div class=\"slides\"></div>" +
		"\t\t\t\t\t\t<a tabindex='-1' class=\"prev\">‹</a>" +
		"\t\t\t\t\t\t<a tabindex='-1' class=\"next\">›</a>" +
		"\t\t\t\t\t\t<a tabindex='-1' class=\"close\">×</a>" +
		"\t\t\t\t\t\t<ol class=\"indicator\"></ol>" +
		"\t\t\t\t\t</div>" +
		"\t\t\t\t</div>";
	// "\t\t\t\t</div>" ;
	if (files.$$.length > 1) {
		html += "\t\t\t<i class=\"fa fa-angle-right jq-right\"></i>";
	}
	html += "\t\t\t</div>"
		+ "\t\t</div>" ;
	return html;
}

//新增的TableList
exports.parseTableList = function(files, fileArray) {
	var descFileList = files.$.desc;
	var fileList = files.$$;
	var html = "<div id=\"sheet1\" class=\"final-sheet\">" +
		"<div class=\"other-padding\">";
	var firstFile = fileList[0].$;
	util.replaceFilePath(firstFile, fileArray);

	var tableHead = "<div class=\"table-list\" name='"+fileList[0].$.name+"' path='"+fileList[0].$.path+"' fileType=\"" + fileList[0].$.type + "\">" +
		"<div class=\"table-list-div\">" +
		"<p class='table-list-p' name='fileList[0].$.name'>"+fileList[0].$.name+"</p>" +
		"</div>" +
		"<div class=\"table-list-right-div\" >\n\n\n\n\n\n\n\n\n";

	if(fileList.length>1){
		tableHead += "<div class='table-list-right-select'><select class=\"input-sm input-s-sm inline report-table-select2\" " +
			"style=\"padding: 0;margin-left:5px;\" onchange=''>";
		for (var i in fileList) {
			var file = fileList[i].$;
			util.replaceFilePath(file, fileArray);
			tableHead+="<option path='"+file.path+"' filetype='"+file.filetype+"' value='"+file.path+"'>" + file.name + "</option>";
		}
		tableHead += "</select></div>\n\n\n\n\n\n\n\n\n";
	}
	tableHead += "<a class=\"table-list-a table-list-download\" href=\"javascript:void(0);\">下载表格</a>" +
		"<a class=\"table-list-a table-list-alldata\" href=\"javascript:void(0);\">查看全部数据</a>" +
		"</div></div>";
	html += tableHead;

	html+= "<div class=\"final-scroll list-table-table\">" +
		"<table class=\"final-table\">";
	var file = fileList[0].$;
	var fileData = parseXml.readFileByNum(file,15);
	if (fileData) {
		var fileList =[];
		if(/\r\n/.test(fileData)){
			fileList= fileData.split('\r\n');
		}else{
			fileList = fileData.split('\n');
		}
		for (var i in fileList) {
			var rowList = fileList[i].split('\t');
			if(rowList.length > 1){
				if (i == 0) {
					html += '<thead>';
				} else {
					html += "<tbody>";
				}
				html += "<tr>";
				for (var k in rowList) {
					html += "<td>" + rowList[k] + "</td>";
				}
				html += "</tr>\n";
				if (i == 0) {
					html += "</thead>";
				} else {
					html += "</tbody>";
				}
			}
		}
		html += "</table></div>";
	}
	if (descFileList) {
		html += "<p class=\"final-title-p\">" + descFileList + "</p>";
	}
	html += "</div></div>";
	return html;
}
//图片路径
exports.getImage = function(path){
	var imagePath = parseXml.getSmallImage(path);
	if(path.indexOf(global.rootPath)==-1){
		path = "/api/v1/app/getImages?imagePath="+imagePath;
	}else{
		path = "/report/report/showjobimgByPath?filepath="+imagePath;
	}
	return path;
}

exports.parsePic =function(file, fileArray, firstImage) {
	var html = "";
	util.replaceFilePath(file, fileArray);
	var imagePath = exports.getImage(file.path);
	var imgHtml = "\t\t\t<img class=\"lazy-load jq-img\" data-original='"+imagePath+"' src=\"\">";
	if (firstImage == 1) {
		imgHtml = "\t\t\t<img class=\"lazy-load jq-img\" src='"+imagePath+"'>";
	}
	html = "<div class=\"other-padding\">" +
		"<div class=\"acdsee-comment-img\">\n" + imgHtml +
		"\t\t\t\t<div class=\"acdsee-comment-word\">\n" +
		"\t\t\t\t\t\t<p class=\"img-comment-word\">" + file.name + "</p>\n" +
		"\t\t\t\t\t\t<p class=\"img-comment-p\">" + file.desc + "</p>\n" +
		"\t\t\t\t</div>\n" +
		"\t</div>\n" +
		"</div>"
	return html;
}
//新轮播图
exports.parsePicList = function(files, fileArray, firstImage, WheelImage){
	var fileList = files.$$;
	if(fileList<=0 || !fileList){
		return "";
	}
	var picdesc = files.$.desc;
	var html = "<div>";
	if(fileList.length==1){
		html += "<div data-thumbnail=\"none\" data-keypress=\"true\" data-autoplay=\"3000\" data-arrows=\"outer\" class=\"raxus-slider\" id=\"wheel_img" + WheelImage + "\">";
	}else{
		html += "<div data-thumbnail=\"bottom\" data-keypress=\"true\"  data-autoplay=\"300\" data-arrows=\"show\" class=\"raxus-slider\" id=\"wheel_img" + WheelImage + "\">";
	}
	html += "\t\t<ul class=\"slider-relative\">\n";

	var count = fileList.length>=10?10:fileList.length;
	for (var i = 0; i < count; i++) {
		var file = fileList[i].$;
		util.replaceFilePath(file ,fileArray);
		var imagePath = file.path;
		imagePath = exports.getImage(imagePath);//parseXml.getSmallImage(imagePath);
		console.log("imagePath:"+imagePath);
		if (firstImage == 1) {
			firstImage++;
			html += "<li class=\"slide wheel\">\n";
			html += "<img class=\"jq-carousel\" data-original=\"" + imagePath
				+ "\" src=\"" + imagePath + "\">";
			html += " <span class=\"text\">\n" +
				"        <small class=\"jq-carousel-filename\">" + file.name + "</small>\n" +
				"    </span>\n";
			html += "</li>\n";
		}else{
			html += "<li class=\"slide wheel\">\n";
			html += "<img class=\"jq-carousel\" data-original=\""
				+ imagePath + "\" src=\"\">";
			html += " <span class=\"text\">\n" +
				"        <small class=\"jq-carousel-filename\">" + file.name + "</small>\n" +
				"    </span>\n";
			html += "</li>\n";
		}
	}
	html += "\t</div>\n";
	if(fileList>=10){
		html += "\t\t<p class=\"final-title-p note-p\">此处实际共有" + fileList.length + "张结果图片，但为了保证浏览报告的流畅性只展示了10张，查看全部图片可以到项目文件中查看，请谅解。</p>\n";
	}
	var picListDesc = ""==picdesc?"":"\t\t<p class=\"final-title-p note-p\">"+picdesc+"</p>\n";
	html += picListDesc +
		"\t</div>\n";

	return html;
}

exports.parseRefList = function(files, fileArray) {
	var html = "</div><div class=\"final-reference\">" +
		"<h5 id=\"reference\" class=\"final-m-title\">参考文献</h5>" +
		"<ul class=\"final-ul\">";
	var refs = files.$$;
	for (var item in refs) {
		var ref = refs[item].$;
		if (!ref.link) {
			html += "<li id=\"ref" + ref.id + "\"><a tabindex='-1' href='javascript:void(0);'>[" + ref.id + "] " + ref.name + "</a></li>";
		} else {
			html += "<li id=\"ref" + ref.id + "\"><a tabindex='-1' target=\"_blank\" href=\"" + ref.link + "\">[" + ref.id + "] " + ref.name + "</a></li>";
		}
	}
	html += "</ul>";
	return html;
}

exports.parseTbale = function(file, fileArray) {
	var html = "<div id=\"sheet1\" class=\"final-sheet\">" +
		"<div class=\"other-padding\">" +
		"<div class=\"final-scroll\">" +
		"<table class=\"final-table\">\n";
	var fileData = parseXml.readFile(file);

	if (fileData) {
		var fileList =[];
		if(/\r\n/.test(fileData)){
			fileList= fileData.split('\r\n');
		}else{
			fileList = fileData.split('\n');
		}
		for (var i in fileList) {
			var rowList = fileList[i].split('\t');
			if(rowList.length > 1){
					if (i == 0) {
					html += '<thead>';
				} else {
					html += "<tbody>";
				}
				html += "<tr>";
				for (var k in rowList) {
					html += "<td>" + rowList[k] + "</td>";
				}
				html += "</tr>\n";
				if (i == 0) {
					html += "</thead>";
				} else {
					html += "</tbody>";
				}
			}
		}
		html += "</table></div>";
		if (file.desc) {
			html += "<p class=\"final-title-p\">" + file.desc + "</p>";
		}
		html += "</div></div>";
		return html;
	}
}

exports.otherHtml = function(){
	return "</div>" +
		"<div class=\"box-right\">\n" +
		"   <div class=\"box-right-content\">\n" +
		"     <div class=\"watch-box\"></div>\n" +
		"	  <div class=\"final-return-top\"><a class=\"return-top\" href=\"#wrapper\"><img class=\"backImg\" src=\"http://www-dev.bmk.local/js/reportHtml/backTop.png\" alt=\"返回按钮\" style=\"display: block;\"></a></div>\n" +
		"	</div>" +
		"</div>"
		+ "\t\t\t</div>\n" +
		"</div></div></div></div>" +
		"<div class=\"final-model jq-model\">\n" +
			"<div class=\"final-model-head\"><a class=\"model-x jq-x\" href=\"javascript:void(0)\">×</a></div>\n" +
			"<div class=\"final-model-body\">\n" +
				"<a tabindex='-1' class=\"model-prev\">‹</a>\n" +
				"<div class=\"body-inner\"></div>\n" +
				"<a tabindex='-1' class=\"model-next\">›</a>\n" +
			"</div>\n" +
			"<div class=\"final-model-foot\"></div>\n" +
		"</div>" +
		"     </div>"+
              "</div>"+
          "</div>"+
      "</div>"+
      "</div>"+
		"<script type=\"text/javascript\" src=\"http://js.biocloud.net/reportHtml/jquery-2.1.1.js\"></script>"+
		"<script type=\"text/javascript\" src=\"http://cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js\"></script>"+
		/*
		"<script type=\"text/javascript\" src=\"http://www-dev.bmk.local/js/reportHtml/reportHtml.js\"></script>"+
*/
		/*"<script type=\"text/javascript\" src=\"static/select2.full.min.js\"></script>" +
		"<script type=\"text/javascript\" src=\"static/jquery-2.1.1.js\"></script>\n" +
		"<script type=\"text/javascript\" src=\"static/newReport.js\"></script>\n" +
		"<script type=\"text/javascript\" src=\"static/raxus-slider.min.js\"></script>\n" +
		"<script type=\"text/javascript\" src=\"/static/js/inside/report/js_new/js/raxus-slider.min.js\"></script>\n"*/


		/*<script type="text/javascript" src="/static/newstatic/jquery-2.1.1.js"></script>
		<script type="text/javascript" src="/static/newstatic/select2.full.min.js"></script>
		<script type="text/javascript" src="/static/newstatic/raxus-slider.min.js"></script>
		<script type="text/javascript" src="/static/newstatic/newReport.js"></script>
		*/
		"<script type=\"text/javascript\" src=\"/static/css/css_new/css/report/select2.min.css\"></script>" +
		"<script type=\"text/javascript\" src=\"/static/js/inside/report/js_new/js/raxus-slider.min.js\"></script>" +
		"<script type=\"text/javascript\" src=\"/static/js/inside/report/js_new/report_html/reporthtml.js\"></script>"+


		"</body>"+
"</html>";
}
