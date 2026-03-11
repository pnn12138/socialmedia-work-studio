/**
 * Unsplash API Provider
 *
 * 封装 Unsplash API 调用，提供高质量免费图片搜索
 * API 文档：https://docs.unsplash.com/
 */

const fetch = require('node-fetch');

// 从环境变量获取 API Key
const ACCESS_KEY = process.env.UNSPLASH_ACCESS_KEY;

if (!ACCESS_KEY) {
  console.warn('Warning: UNSPLASH_ACCESS_KEY not set. Some functionality may not work.');
}

const BASE_URL = 'https://api.unsplash.com';

/**
 * 构建 API 请求头
 * @returns {Object} 请求头
 */
function getHeaders() {
  return {
    'Authorization': `Client-ID ${ACCESS_KEY || ''}`,
    'Accept-Version': 'v1',
  };
}

/**
 * Unsplash 图片搜索
 * @param {string} query - 搜索关键词
 * @param {Object} options - 搜索选项
 * @param {string} options.orientation - 图片方向：portrait | landscape | square
 * @param {string} options.color - 主导颜色
 * @param {string} options.order_by - 排序：relevant | latest
 * @param {number} options.per_page - 每页数量，默认 12，最大 30
 * @param {number} options.page - 页码
 * @returns {Promise<Object>} 标准化搜索结果
 */
async function searchUnsplashImages(query, options = {}) {
  const params = new URLSearchParams();

  params.append('query', query);

  // 添加可选参数
  if (options.orientation) {
    params.append('orientation', options.orientation);
  }

  if (options.color) {
    // Unsplash 支持的颜色值
    const colorMap = {
      red: 'red',
      orange: 'orange',
      yellow: 'yellow',
      green: 'green',
      teal: 'teal',
      blue: 'blue',
      purple: 'purple',
      pink: 'pink',
      white: 'white',
      gray: 'gray',
      black: 'black',
      brown: 'brown',
    };
    if (colorMap[options.color.toLowerCase()]) {
      params.append('color', colorMap[options.color.toLowerCase()]);
    }
  }

  if (options.order_by) {
    params.append('order_by', options.order_by);
  }

  if (options.per_page) {
    params.append('per_page', Math.min(options.per_page, 30)); // Unsplash 限制最大 30
  } else {
    params.append('per_page', 15);
  }

  if (options.page) {
    params.append('page', options.page);
  }

  const url = `${BASE_URL}/search/photos?${params.toString()}`;

  try {
    const response = await fetch(url, {
      headers: getHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Unsplash API Error: ${response.status} - ${errorData.error || response.statusText}`);
    }

    const data = await response.json();

    // 检查速率限制
    const remaining = response.headers.get('X-RateLimit-Remaining');
    if (remaining && parseInt(remaining) < 10) {
      console.warn(`Warning: Unsplash rate limit approaching. Remaining: ${remaining}`);
    }

    const { normalizeSearchResults } = require('../utils/normalize');
    return normalizeSearchResults(data.results, 'unsplash', query);
  } catch (error) {
    console.error('Unsplash API Error:', error.message);
    throw new Error(`Failed to search images from Unsplash: ${error.message}`);
  }
}

/**
 * 获取 Unsplash 精选图片
 * @param {Object} options - 选项
 * @param {string} options.orientation - 图片方向
 * @param {string} options.order_by - 排序
 * @param {number} options.per_page - 每页数量
 * @param {number} options.page - 页码
 * @returns {Promise<Object>} 标准化搜索结果
 */
async function getCuratedPhotos(options = {}) {
  const params = new URLSearchParams();

  if (options.orientation) {
    params.append('orientation', options.orientation);
  }

  if (options.order_by) {
    params.append('order_by', options.order_by);
  }

  if (options.per_page) {
    params.append('per_page', Math.min(options.per_page, 30));
  } else {
    params.append('per_page', 12);
  }

  if (options.page) {
    params.append('page', options.page);
  }

  const url = `${BASE_URL}/photos/curated?${params.toString()}`;

  try {
    const response = await fetch(url, {
      headers: getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Unsplash API Error: ${response.status}`);
    }

    const data = await response.json();
    const { normalizeSearchResults } = require('../utils/normalize');
    return normalizeSearchResults(data, 'unsplash', 'curated');
  } catch (error) {
    console.error('Unsplash API Error:', error.message);
    throw new Error(`Failed to get curated photos from Unsplash: ${error.message}`);
  }
}

/**
 * 获取单张图片详情
 * @param {string} id - 图片 ID
 * @returns {Promise<Object>} 标准化图片数据
 */
async function getPhotoById(id) {
  const url = `${BASE_URL}/photos/${id}`;

  try {
    const response = await fetch(url, {
      headers: getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Unsplash API Error: ${response.status}`);
    }

    const photo = await response.json();
    const { normalizePhoto } = require('../utils/normalize');
    return normalizePhoto(photo, 'unsplash');
  } catch (error) {
    console.error('Unsplash API Error:', error.message);
    throw new Error(`Failed to get photo details from Unsplash: ${error.message}`);
  }
}

/**
 * 获取随机图片
 * @param {Object} options - 选项
 * @param {string} options.query - 搜索关键词
 * @param {string} options.orientation - 图片方向
 * @returns {Promise<Object>} 标准化图片数据
 */
async function getRandomPhoto(options = {}) {
  const params = new URLSearchParams();

  if (options.query) {
    params.append('query', options.query);
  }

  if (options.orientation) {
    params.append('orientation', options.orientation);
  }

  const url = `${BASE_URL}/photos/random?${params.toString()}`;

  try {
    const response = await fetch(url, {
      headers: getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Unsplash API Error: ${response.status}`);
    }

    const photo = await response.json();
    const { normalizePhoto } = require('../utils/normalize');
    return normalizePhoto(photo, 'unsplash');
  } catch (error) {
    console.error('Unsplash API Error:', error.message);
    throw new Error(`Failed to get random photo from Unsplash: ${error.message}`);
  }
}

/**
 * 获取用户/摄影师信息
 * @param {string} username - 用户名
 * @returns {Promise<Object>} 用户信息
 */
async function getUser(username) {
  const url = `${BASE_URL}/users/${username}`;

  try {
    const response = await fetch(url, {
      headers: getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Unsplash API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Unsplash API Error:', error.message);
    throw new Error(`Failed to get user info from Unsplash: ${error.message}`);
  }
}

module.exports = {
  searchUnsplashImages,
  getCuratedPhotos,
  getPhotoById,
  getRandomPhoto,
  getUser,
};
