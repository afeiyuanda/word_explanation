//用户存放工具方法

//返回文件的路径
exports.getFilepath = function(file) {
	return file.substring(0, file.lastIndexOf("/") + 1);
}

//解析file2Dataobject 返回文件集合
exports.getFileNodeArray = function(fileArray, fileToDataObj) {

	if (fileToDataObj.hasOwnProperty('fileNode') || fileToDataObj.hasOwnProperty('folderNode')) {
		recursionFileData(fileArray, fileToDataObj);
	}
}

//递归处理文件

function recursionFileData(fileArray, fileToDataObj) {
	if (Object.prototype.toString.call(fileToDataObj) === '[object Array]') {
		for (var i in fileToDataObj) {
			recursionFileData(fileArray, fileToDataObj[i]);
		}
	} else {
		for (var i in fileToDataObj) {
			if (i == 'folderNode') {
				recursionFileData(fileArray, fileToDataObj[i]);
			}
			if (i == 'fileNode') {
				var fileNodes = fileToDataObj[i];
				for (var j in fileNodes) {
					var fileNode = fileNodes[j];
					fileArray.push(fileNode);
				}
			}
		}
	}
}

//替换单个文件  判断文件的类型,吧另外生成的.cloud的 fileuuid 直接添加到xml中生成
exports.replaceFilePath = function(file, fileArray) {
	if (!file.path) {
		console.log("not find file path ,filename : " + file.name + " filetype:" + filetype + " file desc : " + file.desc);
	}
	var regexp = new RegExp('^\..*' + file.path + '$', 'g');
	if (/^.*\.KEGG\.list$/g.test(file.path) || /^.*\.html/g.test(file.path)) {
		regexp = new RegExp('^.*' + file.path + '.cloud$', 'g');
	}
	for (var item in fileArray) {
		if (regexp.test(fileArray[item].relativePath)) {
			//第二xml中有fileUuid返回id,否则返回全路径
			if(fileArray[item].fileUuid){
				file.path = fileArray[item].fileUuid;
			}else{
				file.path = global.rootPath + file.path;
			}
			break;
		}
	}
	if(file.path && file.path.indexOf(global.rootPath)==-1){
		file.path = global.rootPath + file.path;
	}
}