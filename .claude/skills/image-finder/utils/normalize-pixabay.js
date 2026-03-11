/**
 * Pixabay 图片搜索结果标准化工具
 *
 * 将 Pixabay API 返回格式统一为标准输出格式
 */

/**
 * 标准化单张图片数据
 * @param {Object} hit - Pixabay 原始图片数据
 * @param {string} source - 来源平台标识
 * @returns {Object} 标准化后的图片数据
 */
function normalizePhoto(hit, source) {
  return {
    id: String(hit.id),
    title: hit.tags || hit.user || generateTitle(hit),
    photographer: hit.user || 'Unknown',
    photographer_url: hit.userImageURL || hit.user || '',
    page_url: hit.pageURL || '',
    image_url: hit.largeImageURL || hit.webformatURL || hit.previewURL || '',
    thumb_url: hit.previewURL || hit.webformatURL || '',
    width: hit.imageWidth || hit.width || 0,
    height: hit.imageHeight || hit.height || 0,
    alt: hit.tags || hit.type || '',
    type: hit.type || 'photo', // photo, vector, illustration, etc.
    category: hit.category || '',
    likes: hit.likes || 0,
    downloads: hit.downloads || 0,
    views: hit.views || 0,
  };
}

/**
 * 标准化图片搜索结果
 * @param {Array} hits - 原始图片数组
 * @param {string} source - 来源平台标识
 * @param {string} query - 搜索关键词
 * @returns {Object} 标准化搜索结果
 */
function normalizeSearchResults(hits, source, query) {
  const results = hits.map(hit => normalizePhoto(hit, source));

  return {
    source: source,
    query: query,
    results: results,
  };
}

/**
 * 生成默认标题
 * @param {Object} hit - 图片数据
 * @returns {string} 生成的标题
 */
function generateTitle(hit) {
  const parts = [];

  if (hit.type) {
    parts.push(hit.type);
  }

  if (hit.user) {
    parts.push(`by ${hit.user}`);
  }

  parts.push('on Pixabay');

  return parts.join(' ');
}

module.exports = {
  normalizePhoto,
  normalizeSearchResults,
  generateTitle,
};
