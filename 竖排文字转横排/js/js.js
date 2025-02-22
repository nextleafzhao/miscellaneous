//计算一段文本的行数和最大列数
function calculateLinesAndMaxLength(text) {
    // 使用正则表达式匹配所有换行符，包括Unix的\n和Windows的\r\n
    const newlineRegex = /\r\n|\n/g;
    // 使用split方法根据换行符分割字符串，得到行数组
    const lines = text.split(newlineRegex);
    // 初始化行数和最大列数
    let linesCount = lines.length;
    let maxColumnCount = 0;
    // 遍历每一行，更新最大列数
    lines.forEach(line => {
      // 获取当前行的长度，即列数
      const columnCount = line.length;
      // 如果当前行的列数大于已知的最大列数，则更新最大列数
      if (columnCount > maxColumnCount) {
        maxColumnCount = columnCount;
      }
    });
    // 返回行数和最大列数
    return {
      linesCount: linesCount,
      maxColumnCount: maxColumnCount
    };
  }
  
  //以文字填充矩阵
  function createTextMatrix(text, maxColumns) {
    // 将文本按行分割
    const lines = text.split("\n");
    // 初始化二维数组，大小为行数 x 最大列数，所有元素初始化为空字符串
    const matrix = Array.from({ length: lines.length }, () => Array(maxColumns).fill(""));
    // 遍历每一行
    lines.forEach((line, rowIndex) => {
      const lineLength = line.length;
      // 遍历当前行的每个字符，将其放入二维数组对应的位置
      for (let colIndex = 0; colIndex < lineLength; colIndex++) {
        matrix[rowIndex][colIndex] = line[colIndex];
      }
      // 如果当前行文本长度小于最大列数，使用 "■" 填充剩余部分
      for (let fillIndex = lineLength; fillIndex < maxColumns; fillIndex++) {
        matrix[rowIndex][fillIndex] = "■";
      }
    });
    // 返回生成的二维数组
    return matrix;
  }
  
  //旋转矩阵
  function rotateMatrix(matrix, clockwise) {
    const n = matrix.length;
    const m = matrix[0].length;
    const result2 = [];
    // 创建一个与原矩阵大小相同的新矩阵，用于存放旋转后的结果
    for (let i = 0; i < m; i++) {
      result2.push(new Array(n).fill(0));
    }
    // 根据旋转方向，更新新矩阵的值
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < m; j++) {
        if (clockwise) {
          // 逆时针旋转：新位置是原矩阵的 (m - j - 1, i)
          result2[m - j - 1][i] = matrix[i][j];
        } else {
          // 顺时针旋转：新位置是原矩阵的 (j, n - i - 1)
          result2[j][n - i - 1] = matrix[i][j];
        }
      }
    }
    return result2;
  }
  /* 示例矩阵
  const k = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12]
  ]; */
  
  // 示例使用
  const text = "出戌大巳巳用喜\n行时吉未时丑神\n五日是时亦时东\n鬼破日向吉天北\n死凶午上出乙方\n门酉时列行贵贵\n同时五各宜人神\n在截不方用上西\n东路遇迎子吉南\n南空申喜丑子方\n方亡时神寅寅炷\n勿不月贵卯卯香\n向宜破神辰辰宜";
  const result = calculateLinesAndMaxLength(text);
  console.log("行数：",result.linesCount);
  console.log("最大列数：",result.maxColumnCount);
  // 创建文本矩阵
  const matrix = createTextMatrix(text, result.maxColumnCount);
  // 打印二维数组为文本形式
  matrix.forEach(row => {
    console.log(row.join(""));
  });
  
  // 逆时针旋转90度
  const a = rotateMatrix(matrix, true);
  console.log("逆时针旋转后的矩阵:");
  a.forEach(row => {
      console.log(row.join(""));
    });
  
  
  document.getElementById("rotateMatrix").innerHTML = a.map(row => row.join('')).join('<br>');
  