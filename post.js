const axios = require('axios');

axios.post('https://jwgl.bupt.edu.cn/jsxsd/', {
    userAccount: '2019213232',
    userPassWord: '',
    encoded: 'MjAxOTIxMzIzMg==%%%MDcwODQwMTB3bXo='
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });

  const fs = require('fs');
  const path = require('path');
  const url = path.join('F:\file1\file2\img');
  var filePath = path.resolve('./27670326');
  // 图片的绝对路径

  fs.readdir(url, 'utf8', (err, fileList) => {
      if (err) throw err;
      fileList.forEach((item, index) => {
          let length = item.split('.').length;
          // 获取文件后缀名
          let type = '.' + item.split('.')[length - 1];
          let oldName = item;
          // 新名称,根据需求修改名称，可以使用正则等等
          // 后缀可用之前的type 也可统一自定义
          let newName = index + '.jpg';
          fs.rename(url + oldName, url + newName, (err) => {
              throw err;
          });
      })
  })
