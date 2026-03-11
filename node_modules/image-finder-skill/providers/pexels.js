/**
 * Pexels API Provider
 *
 * 封装 Pexels API 调用，提供统一的图片搜索接口
 */

const { createClient } = require('pexels');
const { normalizeSearchResults } = require('../utils/normalize');

// 从环境变量获取 API Key
const API_KEY = process.env.PEXELS_API_KEY;

if (!API_KEY) {
  console.warn('Warning: PEXELS_API_KEY not set. Some functionality may not work.');
}

// 初始化 Pexels 客户端
const client = createClient(API_KEY || '');

/**
 * Pexels 图片搜索
 * @param {string} query - 搜索关键词
 * @param {Object} options - 搜索选项
 * @param {string} options.orientation - 图片方向：portrait | landscape | square
 * @param {string} options.color - 主导颜色
 * @param {string} options.size - 图片尺寸：small | medium | large
 * @param {number} options.per_page - 每页数量，默认 15，最大 80
 * @param {number} options.page - 页码
 * @returns {Promise<Object>} 标准化搜索结果
 */
async function searchPexelsImages(query, options = {}) {
  const searchOptions = {
    query: query,
  };

  // 添加可选参数
  if (options.orientation) {
    searchOptions.orientation = options.orientation;
  }

  if (options.color) {
    searchOptions.color = options.color;
  }

  if (options.size) {
    searchOptions.size = options.size;
  }

  if (options.per_page) {
    searchOptions.per_page = Math.min(options.per_page, 80); // Pexels 限制最大 80
  }

  if (options.page) {
    searchOptions.page = options.page;
  }

  try {
    const response = await client.photos.search(searchOptions);

    return normalizeSearchResults(
      response.photos,
      'pexels',
      query
    );
  } catch (error) {
    console.error('Pexels API Error:', error.message);
    throw new Error(`Failed to search images from Pexels: ${error.message}`);
  }
}

/**
 * 获取 Pexels 精选图片
 * @param {Object} options - 选项
 * @param {string} options.orientation - 图片方向
 * @param {number} options.per_page - 每页数量
 * @param {number} options.page - 页码
 * @returns {Promise<Object>} 标准化搜索结果
 */
async function searchCuratedPhotos(options = {}) {
  const searchOptions = {};

  if (options.orientation) {
    searchOptions.orientation = options.orientation;
  }

  if (options.per_page) {
    searchOptions.per_page = Math.min(options.per_page, 80);
  }

  if (options.page) {
    searchOptions.page = options.page;
  }

  try {
    const response = await client.photos.curated(searchOptions);

    return normalizeSearchResults(
      response.photos,
      'pexels',
      'curated'
    );
  } catch (error) {
    console.error('Pexels API Error:', error.message);
    throw new Error(`Failed to get curated photos from Pexels: ${error.message}`);
  }
}

/**
 * 获取单张图片详情
 * @param {string} id - 图片 ID
 * @returns {Promise<Object>} 标准化图片数据
 */
async function getPhotoById(id) {
  try {
    const photo = await client.photos.show(id);
    const { normalizePhoto } = require('../utils/normalize');
    return normalizePhoto(photo, 'pexels');
  } catch (error) {
    console.error('Pexels API Error:', error.message);
    throw new Error(`Failed to get photo details from Pexels: ${error.message}`);
  }
}

/**
 * 获取随机图片
 * @returns {Promise<Object>} 标准化图片数据
 */
async function getRandomPhoto() {
  try {
    const photo = await client.photos.random();
    const { normalizePhoto } = require('../utils/normalize');
    return normalizePhoto(photo, 'pexels');
  } catch (error) {
    console.error('Pexels API Error:', error.message);
    throw new Error(`Failed to get random photo from Pexels: ${error.message}`);
  }
}

module.exports = {
  searchPexelsImages,
  searchCuratedPhotos,
  getPhotoById,
  getRandomPhoto,
};
