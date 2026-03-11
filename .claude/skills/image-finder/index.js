/**
 * Image Finder Skill - 主入口文件
 *
 * 统一调用不同图片平台的 Provider
 * 提供平台无关的图片搜索接口
 *
 * 支持的 Provider:
 * - pexels: Pexels API (免费，高质量)
 * - unsplash: Unsplash API (免费，摄影师社区)
 * - pixabay: Pixabay API (免费，多类型)
 * - ai-generator: AI 图像生成 (OpenAI/Replicate)
 */

// 加载根目录 .env 文件
const path = require('path');
const dotenv = require('dotenv');

function findRootEnv() {
  // 从当前文件向上查找 .env 文件
  let currentDir = __dirname;
  for (let i = 0; i < 5; i++) {
    const envPath = path.join(currentDir, '.env');
    if (require('fs').existsSync(envPath)) {
      return envPath;
    }
    currentDir = path.dirname(currentDir);
  }
  return null;
}

const envPath = findRootEnv();
if (envPath) {
  dotenv.config({ path: envPath });
  console.log(`[dotenv] Loaded environment from: ${envPath}`);
} else {
  console.log('[dotenv] No .env file found, using system environment variables');
}

const pexelsProvider = require('./providers/pexels');
const unsplashProvider = require('./providers/unsplash');
const pixabayProvider = require('./providers/pixabay');
const aiGeneratorProvider = require('./providers/ai-generator');

/**
 * 可用的 Provider 列表
 */
const PROVIDERS = {
  pexels: pexelsProvider,
  unsplash: unsplashProvider,
  pixabay: pixabayProvider,
  'ai-generator': aiGeneratorProvider,
};

/**
 * 默认 Provider 优先级（用于自动降级）
 */
const DEFAULT_PROVIDER_ORDER = ['pexels', 'unsplash', 'pixabay'];

/**
 * 速率限制配置（毫秒）
 */
const RATE_LIMITS = {
  pexels: 200,    // Pexels: 200 次/小时
  unsplash: 50,   // Unsplash: 50 次/小时
  pixabay: 1000,  // Pixabay: 100 次/分钟
};

/**
 * 请求延迟记录
 */
const lastRequestTime = {};

/**
 * 应用速率限制延迟
 * @param {string} provider - Provider 名称
 */
async function applyRateLimit(provider) {
  const now = Date.now();
  const lastTime = lastRequestTime[provider] || 0;
  const minInterval = RATE_LIMITS[provider] || 1000;

  if (now - lastTime < minInterval) {
    const delay = minInterval - (now - lastTime);
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  lastRequestTime[provider] = Date.now();
}

/**
 * 统一图片搜索接口 - 支持多源降级
 *
 * @param {string} query - 搜索关键词
 * @param {Object} options - 搜索选项
 * @param {string|string[]} options.provider - 指定 Provider(s)，默认自动选择
 * @param {boolean} options.fallback - 是否启用降级，默认 true
 * @param {string} options.orientation - 图片方向：portrait | landscape | square
 * @param {string} options.color - 主导颜色
 * @param {string} options.size - 图片尺寸
 * @param {number} options.per_page - 返回数量，默认 15
 * @param {number} options.page - 页码，默认 1
 * @param {number} options.min_results - 最小结果数，默认 5
 * @returns {Promise<Object>} 标准化搜索结果
 */
async function searchImages(query, options = {}) {
  const {
    fallback = true,
    min_results = 5,
    ...searchOptions
  } = options;

  // 确定 Provider 列表
  let providersToTry;

  if (options.provider) {
    if (Array.isArray(options.provider)) {
      providersToTry = options.provider;
    } else {
      providersToTry = [options.provider];
    }
  } else if (fallback) {
    // 默认使用降级链
    providersToTry = [...DEFAULT_PROVIDER_ORDER];
  } else {
    providersToTry = [DEFAULT_PROVIDER_ORDER[0]];
  }

  // 过滤出可用的 Provider
  const availableProviders = providersToTry.filter(p => PROVIDERS[p]);

  if (availableProviders.length === 0) {
    throw new Error(`No available providers. Requested: ${providersToTry.join(', ')}`);
  }

  // 尝试每个 Provider 直到成功
  let lastError;

  for (const providerName of availableProviders) {
    try {
      await applyRateLimit(providerName);

      const provider = PROVIDERS[providerName];
      const result = await provider.searchPexelsImages
        ? await provider.searchPexelsImages(query, searchOptions)
        : await provider.searchUnsplashImages
          ? await provider.searchUnsplashImages(query, searchOptions)
          : await provider.searchPixabayImages
            ? await provider.searchPixabayImages(query, searchOptions)
            : await provider.searchImages(query, searchOptions);

      // 检查结果数量是否满足要求
      if (result.results && result.results.length >= min_results) {
        result.used_provider = providerName;
        result.fallback_chain = availableProviders;
        return result;
      }

      // 结果不足但非空，记录并继续尝试
      if (result.results && result.results.length > 0) {
        console.log(`Provider ${providerName} returned ${result.results.length} results (< ${min_results}), trying next provider...`);
        // 保存第一个非空结果作为备用
        if (!lastError) {
          lastError = { partial_result: result };
        }
      }

    } catch (error) {
      console.warn(`Provider ${providerName} failed: ${error.message}`);
      lastError = error;

      // 如果不启用降级，直接抛出错误
      if (!fallback) {
        throw error;
      }
      // 继续尝试下一个 Provider
    }
  }

  // 所有 Provider 都失败或无结果
  if (lastError?.partial_result) {
    // 返回部分结果
    lastError.partial_result.used_provider = lastError.partial_result.source;
    lastError.partial_result.fallback_chain = availableProviders;
    lastError.partial_result.warning = 'Limited results - all providers returned few or no results';
    return lastError.partial_result;
  }

  throw new Error(`All providers failed to search images for "${query}". Tried: ${availableProviders.join(', ')}`);
}

/**
 * 获取精选图片
 *
 * @param {Object} options - 选项
 * @param {string} options.provider - 指定 Provider
 * @param {string} options.orientation - 图片方向
 * @param {number} options.per_page - 返回数量
 * @returns {Promise<Object>} 标准化搜索结果
 */
async function getCuratedPhotos(options = {}) {
  const providerName = options.provider || 'pexels';
  const provider = PROVIDERS[providerName];

  if (!provider) {
    throw new Error(`Unknown provider: ${providerName}. Available: ${Object.keys(PROVIDERS).join(', ')}`);
  }

  await applyRateLimit(providerName);

  const { provider: _, ...curatedOptions } = options;

  if (provider.searchCuratedPhotos) {
    return await provider.searchCuratedPhotos(curatedOptions);
  }

  throw new Error(`Provider ${providerName} does not support curated photos`);
}

/**
 * 通过 ID 获取图片详情
 *
 * @param {string} id - 图片 ID
 * @param {string} options.provider - 指定 Provider
 * @returns {Promise<Object>} 标准化图片数据
 */
async function getPhotoById(id, options = {}) {
  const providerName = options.provider || 'pexels';
  const provider = PROVIDERS[providerName];

  if (!provider) {
    throw new Error(`Unknown provider: ${providerName}`);
  }

  await applyRateLimit(providerName);

  return await provider.getPhotoById(id);
}

/**
 * 获取随机图片
 *
 * @param {string} options.provider - 指定 Provider
 * @param {Object} options - 其他选项
 * @returns {Promise<Object>} 标准化图片数据
 */
async function getRandomPhoto(options = {}) {
  const providerName = options.provider || 'pexels';
  const provider = PROVIDERS[providerName];

  if (!provider) {
    throw new Error(`Unknown provider: ${providerName}`);
  }

  await applyRateLimit(providerName);

  const { provider: _, ...photoOptions } = options;

  return await provider.getRandomPhoto(photoOptions);
}

/**
 * AI 图像生成
 *
 * @param {Object} options - 生成选项
 * @param {string} options.provider - 指定 provider: openai | replicate | auto
 * @param {string} options.prompt - 生成提示词
 * @returns {Promise<Object>} 生成结果
 */
async function generateAIImage(options = {}) {
  return await aiGeneratorProvider.generateImage(options);
}

/**
 * 图像编辑（去背、放大等）
 *
 * @param {string} tool - 工具名称
 * @param {Buffer|string} image - 图像
 * @param {Object} options - 选项
 * @returns {Promise<Buffer>} 处理后的图像
 */
async function editImage(tool, image, options = {}) {
  return await aiGeneratorProvider.useClipDrop(tool, image, options);
}

/**
 * 列出可用的 Provider
 *
 * @returns {string[]} Provider 名称列表
 */
function listProviders() {
  return Object.keys(PROVIDERS);
}

/**
 * 获取 Provider 信息
 *
 * @param {string} providerName - Provider 名称
 * @returns {Object} Provider 信息
 */
function getProviderInfo(providerName) {
  const info = {
    pexels: {
      name: 'Pexels',
      type: 'free',
      rateLimit: '200/hour',
      features: ['search', 'curated', 'random'],
    },
    unsplash: {
      name: 'Unsplash',
      type: 'free',
      rateLimit: '50/hour',
      features: ['search', 'curated', 'random'],
    },
    pixabay: {
      name: 'Pixabay',
      type: 'free',
      rateLimit: '100/minute',
      features: ['search', 'editors_choice'],
    },
    'ai-generator': {
      name: 'AI Image Generator',
      type: 'paid',
      providers: ['OpenAI DALL-E 3', 'Replicate SD'],
      features: ['generate', 'edit'],
    },
  };

  return info[providerName] || { name: providerName, type: 'unknown' };
}

// 导出 API
module.exports = {
  searchImages,
  getCuratedPhotos,
  getPhotoById,
  getRandomPhoto,
  generateAIImage,
  editImage,
  listProviders,
  getProviderInfo,
  PROVIDERS,
};
