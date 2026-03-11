/**
 * Web Assets Fetcher - 官网品牌资产获取
 *
 * 从官方网站获取 Logo、favicon、OG Image 等品牌资产
 */

const https = require('https');
const http = require('http');
const { downloadFile } = require('../downloaders/universal');

/**
 * 获取网页 HTML 内容
 * @param {string} url - 网页 URL
 * @returns {Promise<string>}
 */
async function fetchHtml(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;

    lib.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; material-fetcher)'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

/**
 * 从 HTML 中提取 meta 标签和图片链接
 * @param {string} html - HTML 内容
 * @param {string} baseUrl - 基础 URL（用于解析相对路径）
 * @returns {Object}
 */
function extractAssets(html, baseUrl) {
  const assets = {
    logos: [],
    icons: [],
    ogImages: [],
    screenshots: []
  };

  // 解析 logo 相关链接
  const logoPatterns = [
    /<link[^>]*rel=["']?(?:apple-touch-icon|icon|shortcut icon)[^>]*href=["']?([^"'\s>]+)/gi,
    /<meta[^>]*property=["']?og:image[^>]*content=["']?([^"'\s>]+)/gi,
    /<meta[^>]*content=["']?([^"'\s>]+)["'][^>]*property=["']?og:image/gi,
    /<img[^>]*src=["']?([^"'\s>]*logo[^"'\s>]*)["'][^>]*>/gi,
    /<img[^>]*src=["']?([^"'\s>]*icon[^"'\s>]*)["'][^>]*>/gi
  ];

  for (const pattern of logoPatterns) {
    let match;
    while ((match = pattern.exec(html)) !== null) {
      let url = match[1];

      // 解析相对路径
      if (url.startsWith('//')) {
        url = 'https:' + url;
      } else if (url.startsWith('/')) {
        const urlObj = new URL(baseUrl);
        url = urlObj.origin + url;
      } else if (!url.startsWith('http')) {
        url = new URL(url, baseUrl).href;
      }

      if (match[0].includes('icon') || match[0].includes('apple-touch')) {
        assets.icons.push(url);
      } else if (match[0].includes('og:image')) {
        assets.ogImages.push(url);
      } else {
        assets.logos.push(url);
      }
    }
  }

  // 去重
  assets.logos = [...new Set(assets.logos)];
  assets.icons = [...new Set(assets.icons)];
  assets.ogImages = [...new Set(assets.ogImages)];

  return assets;
}

/**
 * 扫描常见 Logo 路径
 * @param {string} baseUrl - 基础 URL
 * @returns {Promise<Array>}
 */
async function scanCommonLogoPaths(baseUrl) {
  const commonPaths = [
    '/logo.svg',
    '/logo.png',
    '/logo.jpg',
    '/assets/logo.svg',
    '/assets/logo.png',
    '/images/logo.svg',
    '/images/logo.png',
    '/static/logo.svg',
    '/static/logo.png',
    '/brand/logo.svg',
    '/brand/logo.png',
    '/favicon.ico',
    '/favicon.svg',
    '/favicon.png'
  ];

  const found = [];

  for (const path of commonPaths) {
    const url = new URL(path, baseUrl).href;
    // 简单检查，实际使用中应该发起 HEAD 请求验证
    found.push({ url, path });
  }

  return found;
}

/**
 * 主函数：获取官网品牌资产
 * @param {string} url - 官网 URL
 * @param {string} type - 类型：logo|screenshot|all
 * @param {string} outputDir - 输出目录
 */
async function fetchWebAssets(url, type = 'all', outputDir) {
  const results = {
    url,
    type,
    outputDir,
    files: [],
    errors: []
  };

  try {
    // 确保 URL 格式正确
    if (!url.startsWith('http')) {
      url = 'https://' + url;
    }

    // 1. 获取 HTML 并提取资产
    const html = await fetchHtml(url);
    const assets = extractAssets(html, url);

    if (type === 'logo' || type === 'all') {
      // 下载 Logo
      for (const logoUrl of assets.logos) {
        const filename = `logo_${new URL(url).hostname}_${Date.now()}.png`;
        const result = await downloadFile(logoUrl, `${outputDir}/${filename}`);
        if (result.success) {
          results.files.push({ type: 'logo', path: result.path, source: logoUrl });
        }
      }

      // 下载 Icons
      for (const iconUrl of assets.icons) {
        const filename = `icon_${new URL(url).hostname}_${Date.now()}.png`;
        const result = await downloadFile(iconUrl, `${outputDir}/${filename}`);
        if (result.success) {
          results.files.push({ type: 'icon', path: result.path, source: iconUrl });
        }
      }

      // 下载 OG Images
      for (const ogUrl of assets.ogImages) {
        const filename = `og_${new URL(url).hostname}_${Date.now()}.jpg`;
        const result = await downloadFile(ogUrl, `${outputDir}/${filename}`);
        if (result.success) {
          results.files.push({ type: 'og_image', path: result.path, source: ogUrl });
        }
      }
    }

    if (type === 'screenshot' || type === 'all') {
      // 截图功能需要调用 web-screenshot-capture 技能
      // 这里标记为待处理，由主程序协调
      results.screenshotPending = true;
    }

  } catch (error) {
    results.errors.push(error.message);
  }

  return results;
}

module.exports = {
  fetchWebAssets,
  fetchHtml,
  extractAssets,
  scanCommonLogoPaths
};
