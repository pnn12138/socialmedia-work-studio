/**
 * URL Extractor - 从页面提取图片链接
 *
 * 工具函数：解析 HTML 内容，提取所有图片 URL
 */

/**
 * 从 HTML 中提取所有图片链接
 * @param {string} html - HTML 内容
 * @param {string} baseUrl - 基础 URL（用于解析相对路径）
 * @returns {Array<{url: string, src: string, alt?: string}>}
 */
function extractImageUrls(html, baseUrl) {
  const images = [];
  const seen = new Set();

  // 匹配 <img> 标签
  const imgRegex = /<img[^>]*src=["']?([^"'\s>]+)["']?[^>]*(?:alt=["']?([^"']*)["']?)?[^>]*>/gi;
  let match;

  while ((match = imgRegex.exec(html)) !== null) {
    let url = match[1];
    const alt = match[2];

    // 解析相对路径
    url = resolveUrl(url, baseUrl);

    // 去重
    if (!seen.has(url)) {
      seen.add(url);
      images.push({ url, src: 'img', alt });
    }
  }

  // 匹配 <meta property="og:image"> 标签
  const ogImageRegex = /<meta[^>]*content=["']?([^"'\s>]+)["']?[^>]*property=["']?og:image[^>]*>/gi;
  while ((match = ogImageRegex.exec(html)) !== null) {
    let url = match[1];
    url = resolveUrl(url, baseUrl);

    if (!seen.has(url)) {
      seen.add(url);
      images.push({ url, src: 'og:image' });
    }
  }

  // 匹配 <link rel="image_src">
  const linkImageRegex = /<link[^>]*href=["']?([^"'\s>]+)["']?[^>]*rel=["']?image_src[^>]*>/gi;
  while ((match = linkImageRegex.exec(html)) !== null) {
    let url = match[1];
    url = resolveUrl(url, baseUrl);

    if (!seen.has(url)) {
      seen.add(url);
      images.push({ url, src: 'link:image_src' });
    }
  }

  // 匹配 CSS background-image (简单匹配)
  const cssImageRegex = /background-image:\s*url\(["']?([^)"'\s]+)["']?\)/gi;
  while ((match = cssImageRegex.exec(html)) !== null) {
    let url = match[1];
    url = resolveUrl(url, baseUrl);

    if (!seen.has(url)) {
      seen.add(url);
      images.push({ url, src: 'css' });
    }
  }

  return images;
}

/**
 * 解析相对路径为绝对路径
 * @param {string} url - URL（可能是相对路径）
 * @param {string} baseUrl - 基础 URL
 * @returns {string}
 */
function resolveUrl(url, baseUrl) {
  if (url.startsWith('//')) {
    return 'https:' + url;
  }
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url;
  }
  if (url.startsWith('/')) {
    const urlObj = new URL(baseUrl);
    return urlObj.origin + url;
  }
  return new URL(url, baseUrl).href;
}

/**
 * 过滤图片 URL，只保留指定类型
 * @param {Array} images - 图片列表
 * @param {Array<string>} extensions - 允许的扩展名
 * @returns {Array}
 */
function filterByExtension(images, extensions = ['.jpg', '.jpeg', '.png', '.svg', '.webp', '.gif']) {
  return images.filter(img => {
    const urlLower = img.url.toLowerCase();
    // 排除 data URI 和 base64
    if (img.url.startsWith('data:')) return false;
    // 检查扩展名
    return extensions.some(ext => urlLower.includes(ext) || urlLower.endsWith(ext));
  });
}

/**
 * 过滤小尺寸图片
 * @param {Array} images - 图片列表
 * @param {number} minWidth - 最小宽度
 * @returns {Array}
 */
function filterBySize(images, minWidth = 200) {
  // 注意：实际尺寸检查需要下载图片或读取响应头
  // 这里通过 URL 模式进行简单过滤
  return images.filter(img => {
    // 排除明显是小图的 URL 模式
    const excludePatterns = ['/thumb', '/thumbnail', '/small', '/mini', '_50x', '_100x'];
    return !excludePatterns.some(p => img.url.toLowerCase().includes(p));
  });
}

module.exports = {
  extractImageUrls,
  resolveUrl,
  filterByExtension,
  filterBySize
};
