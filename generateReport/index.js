// 使用node.js处理结题报告生成html问题,
/*
    使用方式 node index.js ./configtest.xml ./fileToDatabase.xml >./log.log
                启动文件     配置文件1          配置文件2                 日志
*/
// 参数在接受固定的contest.xml文件和filetodata.xml文件并把两个文件组合生成html
// 原来html是java生成,现在只在项目完成后生成html一次
var parseXml = require('./parseXml.js');
var util = require('./util.js');
var htmlTmpl = require('./htmlTmpl.js');
var rf = require("fs");

var contest_xml;
var fileToData;
var saveFile = '.report.html';
var log = '';
var concfgtestObj;
var fileToDataObj;
var html = '';
var fileArray = [];

// 接受参数
process.argv.forEach(function(val, index, array) {
    if (index == 2) {
        contest_xml = val;
    }
    if (index == 3) {
        fileToData = val;
    }
});
console.log("contest_xml:" + contest_xml);
console.log("fileToData:" + fileToData);
if (!contest_xml && !fileToData) {
    console.log('没有输入文件');
    throw '';
}
global.rootPath = util.getFilepath(contest_xml);
saveFile = util.getFilepath(contest_xml) + '.report.html';
concfgtestObj = eval('(' + parseXml.resultConfig(contest_xml) + ')');
fileToDataObj = eval('(' + parseXml.resultFileData(fileToData) + ')');
if(fileToDataObj){
    util.getFileNodeArray(fileArray, fileToDataObj.rootNode);
}else{
    fileToDataObj = {};
}

var html = '';
var type = "";
var firsttitle = "";
var H3num = 1;
var H2num = 1;
var H1num = 1;
var WheelImage = 1;
var WheelTable = 1;
var firstImage = 1;
var h2number = 1;
for (var i in concfgtestObj.report.$$) {
    if (i == 0) {
        var concfgtestObjHead = {};
        var report_time = "XXXX/XX/XX";
        var report_abstract = "";
        concfgtestObjHead.report_version = concfgtestObj.report.$$[0].$.value;
        concfgtestObjHead.report_name = concfgtestObj.report.$$[1].$.value;
        concfgtestObjHead.report_code = concfgtestObj.report.$$[2].$.value;
        concfgtestObjHead.report_user = concfgtestObj.report.$$[3].$.value;
        concfgtestObjHead.report_user_addr = concfgtestObj.report.$$[4].$.value;

        if(concfgtestObj.report.$$[5].$.value && concfgtestObj.report.$$[5].$.value.split(';').length>=4){
            report_time = concfgtestObj.report.$$[5].$.value.split(';')[3];
        }
        if(concfgtestObj.report.$$[6].$){
            report_abstract = concfgtestObj.report.$$[6].$.value;
        }else if(concfgtestObj.report.$$[7].$.value.indexOf("p-abstract")>-1){
            //微生物有时候会多一个空的<report_abstract  />
            report_abstract = concfgtestObj.report.$$[7].$.value;
        }

        concfgtestObjHead.report_time = report_time;
        concfgtestObjHead.report_abstract = report_abstract;

        html += htmlTmpl.addBodyHeadString(concfgtestObjHead);
    } else if (i > 6) {
        var objectH = concfgtestObj.report.$$[i];
        for (var item in objectH) {
            if (item != '$' && objectH[item] == 'file') {
                html += htmlTmpl.parseFile(objectH.$, fileArray);
                type = 'file';
            } else if (item != '$' && objectH[item] == 'file_list') {
                html += htmlTmpl.parseFileList(objectH, fileArray,WheelTable);
                type = 'file_list';
            }  else if (item != '$' && objectH[item] == 'table_list') {
                html += htmlTmpl.parseTableList(objectH, fileArray);
                type = 'file_list';
            } else if (item != '$' && objectH[item] == 'pic') {
                html += htmlTmpl.parsePic(objectH.$, fileArray, firstImage);
                type = 'pic'
            } else if (item != '$' && objectH[item] == 'h1') {
                if (firsttitle) {
                    html += '</div>';
                }
                html += "<div class=\"acdsee-comment_H1_" + H1num + "\"><h5 id=\"acdsee-comment_H1_" + H1num + "\" class=\"final-m-title\">" + objectH.$.desc + " </h5>";
                type = 'h1';
                firsttitle = 'no';
                H1num++;
            } else if (item != '$' && objectH[item] == 'h2') {
                html += "<p id=\"acdsee-comment_H2_" + H2num + "\" class=\"final-title-bold\">" + objectH.$.desc + "</p>";
                type = 'h2';
                H2num++;
            } else if (item != '$' && objectH[item] == 'h3') {
                //html += "<p id=\"acdsee-comment_H3_" + H2num + "\" class=\"final-title-three\">" + objectH.$.desc + "</p>";
                html += "<p id=\"acdsee-comment_H3_" + H3num + "\" name=\"H2_" + (H2num-1) + "\" class=\"final-title-three\">"
                    + objectH.$.desc + "</p>";
                type = 'h3';
                H3num++;
            } else if (item != '$' && objectH[item] == 'p') {
                html += "<p class=\"final-p\">" + objectH.$.desc + "</p>";
                type = 'p';
            } else if (item != '$' && objectH[item] == 'pic_list') {
                html += htmlTmpl.parsePicList(objectH, fileArray, firstImage, WheelImage);
                type = 'pic_list';
                WheelImage ++;
            } else if (item != '$' && objectH[item] == 'ref_list') {
                html += htmlTmpl.parseRefList(objectH, fileArray);
                type = 'ref_list';
            } else if (item != '$' && objectH[item] == 'table') {
                html += htmlTmpl.parseTbale(objectH.$, fileArray);
                type = 'table';
            }
            if (item == 'h1' && !'图片预览'.test(objectH.$.name)) {
                h2number++;
            }
            if (item == 'h2') {
                h2number++;
            }
        }
    }
}
html += htmlTmpl.otherHtml();
parseXml.saveFile("", saveFile);
parseXml.saveFile(html, saveFile);