/**
 * TextProcessor 类，用于处理文本相关操作
 */
class TextProcessor {
    /**
     * 从每一行中删除尾随空格
     * @param {string} text - 要处理的文本
     * @returns {string} - 处理后的文本
     */
    static removeTrailingWhitespace(text) {
        // 将文本按换行符分割为行数组
        let lines = text.split('\n');
        // 使用 map 方法对每行进行处理，删除尾随空格
        let processedLines = lines.map(line => line.replace(/\s+$/, ''));
        // 将处理后的行数组重新组合为文本
        return processedLines.join('\n');
    }

    /**
     * 从文本中删除空行
     * @param {string} text - 要处理的文本
     * @returns {string} - 处理后的文本
     */
    static removeBlankLines(text) {
        // 将文本按换行符分割为行数组
        let lines = text.split('\n');
        // 使用 filter 方法筛选出非空行
        let nonBlankLines = lines.filter(line => line.trim().length > 0);
        // 将非空行数组重新组合为文本
        return nonBlankLines.join('\n');
    }

    /**
     * 综合处理文本，先删除行尾空白符，再删除空行
     * @param {string} text - 要处理的文本
     * @returns {string} - 最终处理后的文本
     */
    static processText(text) {
        // 先调用 removeTrailingWhitespace 方法删除行尾空白符
        let textWithoutTrailingWhitespace = this.removeTrailingWhitespace(text);
        // 再调用 removeBlankLines 方法删除空行
        return this.removeBlankLines(textWithoutTrailingWhitespace);
    }
}

/**
 * StringMatrixCreator 类，用于处理字符串相关操作
 */
class StringMatrixCreator {
    /**
     * 构造函数，目前为空
     */
    constructor() { }

    /**
     * 计算字符串中的行数
     * @param {string} str - 输入的字符串
     * @returns {number} - 行数
     * @throws {Error} - 如果输入不是字符串，抛出错误
     */
    countLines(str) {
        if (typeof str !== 'string') {
            throw new Error('输入必须是字符串');
        }
        return str.split('\n').length;
    }

    /**
     * 找出字符串中最长的行
     * @param {string} str - 输入的字符串
     * @returns {string} - 最长的行
     * @throws {Error} - 如果输入不是字符串，抛出错误
     */
    findLongestLine(str) {
        if (typeof str !== 'string') {
            throw new Error('输入必须是字符串');
        }
        const lines = str.split('\n');
        let maxLength = 0;
        let longestLine = '';
        for (const line of lines) {
            if (line.length > maxLength) {
                maxLength = line.length;
                longestLine = line;
            }
        }
        return longestLine;
    }

    /**
     * 根据输入字符串创建矩阵
     * @param {string} str - 输入的字符串
     * @returns {string[]} - 表示矩阵的字符串数组
     * @throws {Error} - 如果输入不是字符串，抛出错误
     */
    createMatrix(str) {
        if (typeof str !== 'string') {
            throw new Error('输入必须是字符串');
        }
        const numLines = this.countLines(str);
        const longestLine = this.findLongestLine(str);
        const colCount = longestLine.length;
        const matrix = [];
        const lines = str.split('\n');
        for (const line of lines) {
            const paddingLength = colCount - line.length;
            const paddedLine = line + '※'.repeat(paddingLength);
            matrix.push(paddedLine);
        }
        return matrix;
    }
}


try {
    const creator = new StringMatrixCreator();

    const inputString = `出巳用喜
   行时吉未时丑
  五日是时亦时东

   `;

    let processedMultiLineText = TextProcessor.processText(inputString);
    console.log(processedMultiLineText);

    //console.log(creator.createMatrix(processedMultiLineText));
    creator.createMatrix(processedMultiLineText).forEach(row => {
        console.log(`${row}`);
    });
} catch (error) {
    console.error(error.message);
}