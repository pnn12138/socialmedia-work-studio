/**
 * AI Image Generator Provider
 *
 * 整合多个 AI 图像生成 API：
 * - OpenAI DALL-E 3 / GPT-Image
 * - Replicate Stable Diffusion
 * - ClipDrop API
 *
 * API 文档：
 * - OpenAI: https://platform.openai.com/docs/api-reference/images
 * - Replicate: https://replicate.com/docs/api
 * - ClipDrop: https://clipdrop.co/apis
 */

const fetch = require('node-fetch');

// 从环境变量获取 API Keys
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const REPLICATE_API_KEY = process.env.REPLICATE_API_TOKEN;
const CLIPDROP_API_KEY = process.env.CLIPDROP_API_KEY;

/**
 * 使用 OpenAI 生成图像
 * @param {Object} options - 生成选项
 * @param {string} options.prompt - 生成提示词
 * @param {string} options.model - 模型：dall-e-3 | dall-e-2
 * @param {string} options.size - 图像尺寸：1024x1024 | 1024x1792 | 1792x1024
 * @param {string} options.quality - 质量：standard | hd
 * @param {string} options.style - 风格：vivid | natural
 * @param {number} options.n - 生成数量
 * @returns {Promise<Object>} 生成结果
 */
async function generateWithOpenAI(options) {
  if (!OPENAI_API_KEY) {
    throw new Error('OPENAI_API_KEY not set in environment variables');
  }

  const payload = {
    model: options.model || 'dall-e-3',
    prompt: options.prompt,
    n: options.n || 1,
    size: options.size || '1024x1024',
  };

  if (options.quality) {
    payload.quality = options.quality;
  }

  if (options.style) {
    payload.style = options.style;
  }

  // DALL-E 3 不支持 user 参数用于图片生成
  // if (options.user) {
  //   payload.user = options.user;
  // }

  try {
    const response = await fetch('https://api.openai.com/v1/images/generations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`OpenAI API Error: ${response.status} - ${error.error?.message || response.statusText}`);
    }

    const data = await response.json();

    return {
      source: 'openai',
      model: payload.model,
      prompt: options.prompt,
      images: data.data.map(img => ({
        url: img.url,
        revised_prompt: img.revised_prompt || options.prompt,
        b64_json: img.b64_json || null,
      })),
      created_at: data.created,
    };
  } catch (error) {
    console.error('OpenAI API Error:', error.message);
    throw error;
  }
}

/**
 * 使用 Replicate 生成图像（Stable Diffusion 等）
 * @param {Object} options - 生成选项
 * @param {string} options.prompt - 生成提示词
 * @param {string} options.version - 模型版本 ID
 * @param {Object} options.input - 额外输入参数
 * @returns {Promise<Object>} 生成结果
 */
async function generateWithReplicate(options) {
  if (!REPLICATE_API_KEY) {
    throw new Error('REPLICATE_API_TOKEN not set in environment variables');
  }

  const version = options.version || 'stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea351df4979778f7e9332fd5ab';

  const payload = {
    version: version,
    input: {
      prompt: options.prompt,
      ...options.input,
    },
  };

  try {
    // 创建预测（异步）
    const createResponse = await fetch('https://api.replicate.com/v1/predictions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${REPLICATE_API_KEY}`,
        'Prefer': 'wait', // 同步等待完成
      },
      body: JSON.stringify(payload),
    });

    if (!createResponse.ok) {
      const error = await createResponse.json();
      throw new Error(`Replicate API Error: ${createResponse.status} - ${error.detail || createResponse.statusText}`);
    }

    const prediction = await createResponse.json();

    // 等待预测完成
    let result = prediction;
    while (result.status === 'processing') {
      await new Promise(resolve => setTimeout(resolve, 2000));
      const statusResponse = await fetch(result.urls.get, {
        headers: {
          'Authorization': `Token ${REPLICATE_API_KEY}`,
        },
      });
      result = await statusResponse.json();
    }

    if (result.status !== 'succeeded') {
      throw new Error(`Replicate generation failed: ${result.error || result.logs}`);
    }

    return {
      source: 'replicate',
      model: version,
      prompt: options.prompt,
      images: result.output.map(url => ({
        url: url,
      })),
      created_at: result.created_at,
    };
  } catch (error) {
    console.error('Replicate API Error:', error.message);
    throw error;
  }
}

/**
 * 使用 ClipDrop 进行图像编辑（去背、放大等）
 * @param {string} tool - 工具名称：remove-background | upscale | relight
 * @param {Buffer|string} image - 图像文件或 URL
 * @param {Object} options - 额外选项
 * @returns {Promise<Buffer>} 处理后的图像
 */
async function useClipDrop(tool, image, options = {}) {
  if (!CLIPDROP_API_KEY) {
    throw new Error('CLIPDROP_API_KEY not set in environment variables');
  }

  const endpoints = {
    'remove-background': 'remove-background/v1',
    'upscale': 'upscale/v1/upscale',
    'relight': 'reimagine/v1',
  };

  const endpoint = endpoints[tool];
  if (!endpoint) {
    throw new Error(`Unknown ClipDrop tool: ${tool}`);
  }

  const formData = new FormData();

  // 处理图像输入
  if (typeof image === 'string') {
    // URL 或文件路径
    if (image.startsWith('http')) {
      // URL - 需要先下载
      const imageResponse = await fetch(image);
      const blob = await imageResponse.blob();
      formData.append('image_file', blob, 'image.jpg');
    } else {
      // 文件路径 - 需要读取
      const fs = require('fs');
      const fileData = fs.readFileSync(image);
      const blob = new Blob([fileData]);
      formData.append('image_file', blob, 'image.jpg');
    }
  } else if (Buffer.isBuffer(image)) {
    const blob = new Blob([image]);
    formData.append('image_file', blob, 'image.jpg');
  } else {
    throw new Error('Invalid image input. Must be URL, file path, or Buffer.');
  }

  // 添加额外选项
  Object.keys(options).forEach(key => {
    formData.append(key, options[key]);
  });

  try {
    const response = await fetch(`https://clipdrop-api.co/${endpoint}`, {
      method: 'POST',
      headers: {
        'x-api-key': CLIPDROP_API_KEY,
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`ClipDrop API Error: ${response.status} - ${error}`);
    }

    // 返回 Buffer
    const arrayBuffer = await response.arrayBuffer();
    return Buffer.from(arrayBuffer);
  } catch (error) {
    console.error('ClipDrop API Error:', error.message);
    throw error;
  }
}

/**
 * 统一的图像生成接口 - 自动选择最佳可用服务
 * @param {Object} options - 生成选项
 * @param {string} options.provider - 指定 provider：openai | replicate | auto
 * @param {string} options.prompt - 生成提示词
 * @returns {Promise<Object>} 生成结果
 */
async function generateImage(options = {}) {
  const provider = options.provider || 'auto';

  if (provider === 'openai' || (provider === 'auto' && OPENAI_API_KEY)) {
    try {
      return await generateWithOpenAI(options);
    } catch (error) {
      if (provider === 'openai') throw error;
      console.warn('OpenAI failed, trying Replicate...');
    }
  }

  if (provider === 'replicate' || (provider === 'auto' && REPLICATE_API_KEY)) {
    try {
      return await generateWithReplicate(options);
    } catch (error) {
      if (provider === 'replicate') throw error;
      console.warn('Replicate failed.');
    }
  }

  throw new Error('All AI image generators are unavailable. Please check API keys.');
}

module.exports = {
  generateWithOpenAI,
  generateWithReplicate,
  useClipDrop,
  generateImage,
};
