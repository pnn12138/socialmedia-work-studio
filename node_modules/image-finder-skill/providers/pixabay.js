/**
 * Pixabay API Provider
 *
 * 封装 Pixabay API 调用，提供完全免费的图片、插画、矢量图搜索
 * API 文档：https://pixabay.com/api/docs/
 */

const fetch = require('node-fetch');

// 从环境变量获取 API Key
const API_KEY = process.env.PIXABAY_API_KEY;

if (!API_KEY) {
  console.warn('Warning: PIXABAY_API_KEY not set. Some functionality may not work.');
}

const BASE_URL = 'https://pixabay.com/api';

/**
 * Pixabay 图片搜索
 * @param {string} query - 搜索关键词
 * @param {Object} options - 搜索选项
 * @param {string} options.category - 分类：backgrounds | fashion | nature | etc.
 * @param {string} options.image_type - 图片类型：all | photo | vector | illustration | etc.
 * @param {string} options.orientation - 图片方向：any | horizontal | vertical
 * @param {string} options.color - 主导颜色
 * @param {string} options.editors_choice - 是否精选：true | false
 * @param {number} options.per_page - 每页数量，默认 20，最大 100
 * @param {number} options.page - 页码
 * @param {number} options.min_width - 最小宽度
 * @param {number} options.min_height - 最小高度
 * @returns {Promise<Object>} 标准化搜索结果
 */
async function searchPixabayImages(query, options = {}) {
  const params = new URLSearchParams();

  params.append('key', API_KEY || '');
  params.append('q', query);

  // 添加可选参数
  if (options.category) {
    params.append('category', options.category);
  }

  if (options.image_type) {
    params.append('image_type', options.image_type);
  }

  if (options.orientation) {
    // Pixabay 使用 horizontal/vertical，需要转换
    const orientationMap = {
      portrait: 'vertical',
      landscape: 'horizontal',
      square: 'horizontal',
      any: 'any',
    };
    if (orientationMap[options.orientation]) {
      params.append('orientation', orientationMap[options.orientation]);
    }
  }

  if (options.color) {
    // Pixabay 支持的颜色值
    const colorMap = {
      red: 'ff0000',
      orange: 'ffa500',
      yellow: 'ffff00',
      green: '008000',
      teal: '008080',
      blue: '0000ff',
      purple: '800080',
      pink: 'ffc0cb',
      white: 'ffffff',
      gray: '808080',
      black: '000000',
      brown: 'a52a2a',
    };
    if (colorMap[options.color.toLowerCase()]) {
      params.append('colors', colorMap[options.color.toLowerCase()]);
    }
  }

  if (options.editors_choice) {
    params.append('editors_choice', options.editors_choice ? 'true' : 'false');
  }

  if (options.per_page) {
    params.append('per_page', Math.min(options.per_page, 100)); // Pixabay 限制最大 100
  } else {
    params.append('per_page', 20);
  }

  if (options.page) {
    params.append('page', options.page);
  }

  if (options.min_width) {
    params.append('min_width', options.min_width);
  }

  if (options.min_height) {
    params.append('min_height', options.min_height);
  }

  const url = `${BASE_URL}/?${params.toString()}`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Pixabay API Error: ${response.status} - ${errorData.message || response.statusText}`);
    }

    const data = await response.json();

    // Pixabay 速率限制检查（每 60 秒 100 次）
    // API 返回头中包含限制信息，但需要应用层实现节流

    const { normalizeSearchResults } = require('../utils/normalize-pixabay');
    return normalizeSearchResults(data.hits, 'pixabay', query);
  } catch (error) {
    console.error('Pixabay API Error:', error.message);
    throw new Error(`Failed to search images from Pixabay: ${error.message}`);
  }
}

/**
 * 获取精选图片（编辑选择）
 * @param {Object} options - 选项
 * @param {string} options.orientation - 图片方向
 * @param {number} options.per_page - 每页数量
 * @param {number} options.page - 页码
 * @returns {Promise<Object>} 标准化搜索结果
 */
async function getEditorsChoicePhotos(options = {}) {
  return searchPixabayImages('', {
    ...options,
    editors_choice: true,
    image_type: 'photo',
  });
}

/**
 * 获取单张图片详情（Pixabay 不需要单独的图片详情接口）
 * @param {string} id - 图片 ID（Pixabay 使用 ID 作为标识）
 * @returns {Promise<Object>} 标准化图片数据
 */
async function getPhotoById(id) {
  // Pixabay 没有单独的图片详情 API，使用搜索接口通过 ID 过滤
  const params = new URLSearchParams();
  params.append('key', API_KEY || '');
  params.append('id', id);

  const url = `${BASE_URL}/?${params.toString()}`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Pixabay API Error: ${response.status}`);
    }

    const data = await response.json();

    if (data.hits && data.hits.length > 0) {
      const { normalizePhoto } = require('../utils/normalize-pixabay');
      return normalizePhoto(data.hits[0], 'pixabay');
    }

    throw new Error(`Photo not found: ${id}`);
  } catch (error) {
    console.error('Pixabay API Error:', error.message);
    throw new Error(`Failed to get photo details from Pixabay: ${error.message}`);
  }
}

/**
 * 获取随机图片（Pixabay 没有随机接口，使用搜索模拟）
 * @param {Object} options - 选项
 * @returns {Promise<Object>} 标准化图片数据
 */
async function getRandomPhoto(options = {}) {
  const randomKeywords = ['nature', 'landscape', 'abstract', 'texture', 'pattern'];
  const randomKeyword = randomKeywords[Math.floor(Math.random() * randomKeywords.length)];

  const results = await searchPixabayImages(options.query || randomKeyword, {
    per_page: 1,
    page: Math.floor(Math.random() * 10) + 1,
  });

  if (results.results && results.results.length > 0) {
    return results.results[0];
  }

  throw new Error('Failed to get random photo from Pixabay');
}

module.exports = {
  searchPixabayImages,
  getEditorsChoicePhotos,
  getPhotoById,
  getRandomPhoto,
};
