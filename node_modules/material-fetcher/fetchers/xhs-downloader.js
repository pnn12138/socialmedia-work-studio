/**
 * XHS Downloader - 小红书笔记图片下载
 *
 * ⚠️ 此模块需要扩展 xiaohongshu-mcp 服务
 * 当前为占位实现，展示接口设计
 */

const { downloadFiles } = require('../downloaders/universal');

/**
 * 调用 xiaohongshu-mcp 获取笔记详情
 * 需要 MCP 服务添加 download_images 工具
 *
 * @param {string} feedId - 笔记 ID
 * @param {string} xsecToken - 安全令牌
 * @returns {Promise<Object>}
 */
async function getFeedDetail(feedId, xsecToken) {
  // TODO: 调用 xiaohongshu-mcp 的 get_feed_detail 工具
  // 当前为模拟实现

  console.log('[XHS Downloader] 获取笔记详情...');
  console.log(`  feed_id: ${feedId}`);
  console.log(`  xsec_token: ${xsecToken}`);

  // 模拟返回结构（实际应从 MCP 服务获取）
  throw new Error(
    '小红书图片下载需要扩展 xiaohongshu-mcp 服务。\n' +
    '请在 xiaohongshu-mcp 服务中添加 download_images 工具。\n' +
    '参考：CLAUDE.md 中的实现指南'
  );
}

/**
 * 从笔记 URL 中提取 feed_id 和 xsec_token
 * @param {string} url - 小红书笔记 URL
 * @returns {Object}
 */
function parseNoteUrl(url) {
  // 支持格式：
  // https://www.xiaohongshu.com/explore/664a0f03000000002f006f9e
  // https://www.xiaohongshu.com/discovery/item/664a0f03000000002f006f9e

  const patterns = [
    /explore\/([a-f0-9]+)/i,
    /item\/([a-f0-9]+)/i,
    /^([a-f0-9]+)$/i  // 直接是 feed_id
  ];

  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) {
      return {
        feedId: match[1],
        xsecToken: null // 需要从详情接口获取
      };
    }
  }

  throw new Error('无法解析小红书笔记 URL');
}

/**
 * 主函数：下载小红书笔记图片
 * @param {string} input - 笔记 ID 或 URL
 * @param {string} outputDir - 输出目录
 * @returns {Promise<Object>}
 */
async function downloadXhsImages(input, outputDir) {
  const results = {
    input,
    outputDir,
    files: [],
    errors: []
  };

  try {
    // 解析输入
    const { feedId, xsecToken } = parseNoteUrl(input);

    // 获取笔记详情（包含图片 URL 列表）
    const detail = await getFeedDetail(feedId, xsecToken);

    // 提取图片 URL
    const images = detail.images || [];
    if (images.length === 0) {
      throw new Error('该笔记没有图片');
    }

    console.log(`[XHS Downloader] 找到 ${images.length} 张图片`);

    // 生成文件名并下载
    const filesToDownload = images.map((url, index) => ({
      url: url,
      filename: `xhs_${feedId}_${index + 1}.jpg`
    }));

    const downloadResult = await downloadFiles(filesToDownload, outputDir);

    results.files = downloadResult.results
      .filter(r => r.success)
      .map(r => ({ type: 'xhs_image', path: r.path }));

    results.errors = downloadResult.results
      .filter(r => !r.success)
      .map(r => `${r.filename}: ${r.error}`);

  } catch (error) {
    results.errors.push(error.message);
  }

  return results;
}

module.exports = {
  downloadXhsImages,
  parseNoteUrl,
  getFeedDetail
};
