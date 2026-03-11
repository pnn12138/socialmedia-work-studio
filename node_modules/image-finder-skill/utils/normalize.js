/**
 * 图片搜索结果标准化工具
 *
 * 将不同图片平台的返回格式统一为标准输出格式
 */

/**
 * 标准化单张图片数据
 * @param {Object} photo - 原始图片数据
 * @param {string} source - 来源平台标识
 * @returns {Object} 标准化后的图片数据
 */
function normalizePhoto(photo, source) {
  return {
    id: String(photo.id),
    title: photo.alt || photo.title || generateTitle(photo),
    photographer: photo.photographer || photo.user?.name || 'Unknown',
    photographer_url: photo.photographer_url || photo.user?.url || '',
    page_url: photo.url || '',
    image_url: photo.src?.original || photo.urls?.regular || photo.largeImageURL || '',
    thumb_url: photo.src?.small || photo.src?.tiny || photo.previewURL || '',
    width: photo.width || 0,
    height: photo.height || 0,
    alt: photo.alt || photo.description || '',
    avg_color: photo.avg_color || '',
  };
}

/**
 * 标准化图片搜索结果
 * @param {Array} photos - 原始图片数组
 * @param {string} source - 来源平台标识
 * @param {string} query - 搜索关键词
 * @returns {Object} 标准化搜索结果
 */
function normalizeSearchResults(photos, source, query) {
  const results = photos.map(photo => normalizePhoto(photo, source));

  return {
    source: source,
    query: query,
    results: results,
  };
}

/**
 * 生成默认标题
 * @param {Object} photo - 图片数据
 * @returns {string} 生成的标题
 */
function generateTitle(photo) {
  const parts = [];

  if (photo.alt) {
    return photo.alt;
  }

  if (photo.photographer) {
    parts.push(`Photo by ${photo.photographer}`);
  }

  parts.push('on Pexels');

  return parts.join(' ');
}

module.exports = {
  normalizePhoto,
  normalizeSearchResults,
  generateTitle,
};
