/**
 * Universal Downloader - 通用下载器
 *
 * 提供统一的文件下载接口，支持 HTTP/HTTPS URL 下载
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

/**
 * 从 URL 下载文件到本地
 * @param {string} url - 文件 URL
 * @param {string} dest - 目标路径
 * @returns {Promise<{success: boolean, path?: string, error?: string}>}
 */
async function downloadFile(url, dest) {
  return new Promise((resolve) => {
    // 确保目标目录存在
    const dir = path.dirname(dest);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // 选择正确的协议模块
    const lib = url.startsWith('https') ? https : http;

    const request = lib.get(url, (response) => {
      // 处理重定向
      if (response.statusCode === 301 || response.statusCode === 302) {
        downloadFile(response.headers.location, dest).then(resolve);
        return;
      }

      if (response.statusCode !== 200) {
        resolve({
          success: false,
          error: `下载失败：HTTP ${response.statusCode}`
        });
        return;
      }

      const file = fs.createWriteStream(dest);
      response.pipe(file);

      file.on('finish', () => {
        file.close();
        resolve({
          success: true,
          path: dest
        });
      });
    });

    request.on('error', (err) => {
      fs.unlink(dest, () => {}); // 删除未完成文件
      resolve({
        success: false,
        error: err.message
      });
    });

    // 设置超时
    request.setTimeout(30000, () => {
      request.destroy();
      fs.unlink(dest, () => {});
      resolve({
        success: false,
        error: '下载超时'
      });
    });
  });
}

/**
 * 批量下载文件
 * @param {Array<{url: string, filename: string}>} files - 文件列表
 * @param {string} outputDir - 输出目录
 * @returns {Promise<{success: boolean, results: Array<{filename: string, success: boolean, path?: string, error?: string}>}>}
 */
async function downloadFiles(files, outputDir) {
  const results = [];

  for (const file of files) {
    const dest = path.join(outputDir, file.filename);
    const result = await downloadFile(file.url, dest);
    results.push({
      filename: file.filename,
      ...result
    });
  }

  const allSuccess = results.every(r => r.success);
  return {
    success: allSuccess,
    results
  };
}

/**
 * 生成安全的文件名
 * @param {string} url - 原始 URL
 * @param {string} prefix - 文件名前缀
 * @returns {string}
 */
function generateFilename(url, prefix = '') {
  const urlObj = new URL(url);
  const pathname = urlObj.pathname.split('/').pop() || 'file';
  const ext = path.extname(pathname) || '.jpg';
  const timestamp = Date.now();

  // 清理文件名中的非法字符
  const safeName = pathname.replace(/[^a-zA-Z0-9._-]/g, '_');

  return `${prefix}${timestamp}_${safeName}`;
}

module.exports = {
  downloadFile,
  downloadFiles,
  generateFilename
};
