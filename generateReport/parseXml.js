//解析xml ,保存xml

//解析xml文件成json

var parseXml = require('xml2js').parseString;
var rf = require("fs");
var select = require("xpath.js");
var dom = require("xmldom").DOMParser;

//解析xml文件读取成object configtest.xml
exports.resultConfig = function(xml) {
	var resultObject;
	try {
		if (xml) {
			var data = rf.readFileSync(xml, "utf-8");
			var doc = new dom().parseFromString(data);
			var nodes = select(doc, "//add");
			parseXml(doc, {
				explicitArray: false,
				explicitChildren: true,
				preserveChildrenOrder: true
			}, function(err, result) {
				// console.log(result);
				resultObject = JSON.stringify(result);
			});
		}
	} catch (e) {
		console.info('解析configtest.xml文件失败');
		console.info(e);
	}
	console.log("解析xml :" + xml + "成功!");
	return resultObject;
}

//解析 file.xml
exports.resultFileData = function(xml) {
	var resultObject;
	try {
		if (xml) {
			var data = rf.readFileSync(xml, "utf-8");
			var doc = new dom().parseFromString(data);
			var nodes = select(doc, "//add");
			parseXml(doc, {
				explicitArray: false,
				preserveChildrenOrder: true
			}, function(err, result) {
				// console.log(result);
				resultObject = JSON.stringify(result);
			});
		}
	} catch (e) {
		console.info('解析file2data.xml文件失败');
		console.info(e);
	}
	console.log("解析xml :" + xml + "成功!");
	return resultObject;
}

//保存文件
exports.saveFile = function(html, path) {
	rf.writeFile(path, html, function(err, result) {
		console.log(err);
	});
	console.info("保存文件 :" + path + "成功");
}

//读取文件
exports.readFile = function(file) {
	// return rf.readFileSync(global.rootPath +'/base_error.xls', 'UTF-8');
	try {
		console.info("读取文件: " + file.path);
		return rf.readFileSync(global.rootPath + file.path, 'UTF-8');
	} catch (e) {
		console.info('读取文件失败' + e);
	}

}
//读num行文件
exports.readFileByNum = function(file,num) {
	try {
		var path = file.path;
		if(file.path && file.path.indexOf(global.rootPath)==-1){
			path = global.rootPath + file.path;
		}
		console.info("读取文件: " + path);
		var data = rf.readFileSync(path, 'UTF-8');
		var subStr = "";
		if(/\r\n/.test(data) && data.split("\r\n").length>0){
			subStr = "\r\n";
		}else if(/\n/.test(data) && data.split("\n").length>0){
			subStr = "\n";
		}
		if(subStr!=""){
			var newData = "";
			var list = data.split(subStr);
			for(var i=0;(i<list.length && i<=num);i++){
				newData += list[i]+subStr;
			}
			data = newData;
		}
		//console.log(data);
		return data;
	} catch (e) {
		console.info('读取文件失败' + e);
		return "";
	}
}
//获取小图
exports.getSmallImage = function(imgPath){
	if(""==imgPath || imgPath.lastIndexOf(".")<=0){
		return imgPath;
	}
	var path1 = imgPath.substring(0,imgPath.lastIndexOf("."));
	var typeName = imgPath.substring(imgPath.lastIndexOf("."),imgPath.length);
	var smallImagePath = path1 + "_small" + typeName;
	try{
		rf.accessSync(smallImagePath,rf.F_OK);
	}catch(e){
		/*console.log(e);*/
		console.log(smallImagePath + ' not exists.');
		return imgPath;
	}
	return smallImagePath;
}
//判断文件是否存在
exports.ifFileExit =  function(filePath){
	try{
		rf.accessSync(filePath,rf.F_OK);
		return true;
	}catch(e){
		/*console.log(e);*/
		console.log(filePath + ' not exists.');
		return false;
	}
}
