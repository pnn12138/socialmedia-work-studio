/**
 * GitHub Fetcher - GitHub 资源获取
 *
 * 从 GitHub 仓库获取 Logo、截图、Assets 等资源
 */

const https = require('https');
const http = require('http');
const { downloadFile, downloadFiles } = require('../downloaders/universal');

// GitHub API 基础 URL
const GITHUB_API = 'https://api.github.com';

/**
 * 从 GitHub 仓库获取文件列表
 * @param {string} repo - 仓库名（格式：user/repo）
 * @param {string} token - GitHub Token（可选）
 * @returns {Promise<Array>}
 */
async function fetchRepoFiles(repo, token = null) {
  const url = `${GITHUB_API}/repos/${repo}/contents`;

  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const options = {
      headers: {
        'User-Agent': 'material-fetcher',
        'Accept': 'application/vnd.github.v3+json'
      }
    };

    if (token) {
      options.headers['Authorization'] = `token ${token}`;
    }

    lib.get(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          // GitHub API 可能返回对象（如错误）或数组
          const files = Array.isArray(parsed) ? parsed : [];
          console.log(`[GitHub Fetcher] 获取到 ${files.length} 个文件`);
          resolve(files);
        } catch (e) {
          console.error('[GitHub Fetcher] 解析失败:', data.substring(0, 200));
          reject(new Error(`解析失败：${e.message}`));
        }
      });
    }).on('error', (err) => {
      console.error('[GitHub Fetcher] 请求错误:', err.message);
      reject(err);
    });
  });
}

/**
 * 识别潜在的 Logo 文件
 * @param {Array} files - 文件列表
 * @returns {Array}
 */
function identifyLogoFiles(files) {
  const logoPatterns = ['logo', 'icon', 'brand', 'avatar'];
  const imageExts = ['.svg', '.png', '.jpg', '.jpeg', '.webp'];

  return files.filter(file => {
    if (file.type !== 'file') return false;

    const name = file.name.toLowerCase();
    const isImage = imageExts.some(ext => name.endsWith(ext));
    const isLogo = logoPatterns.some(p => name.includes(p));

    return isImage && (isLogo || name.startsWith('logo') || name.startsWith('icon'));
  });
}

/**
 * 从 README 中提取图片链接
 * @param {string} repo - 仓库名
 * @param {string} token - GitHub Token
 * @returns {Promise<Array>}
 */
async function extractImagesFromReadme(repo, token = null) {
  const url = `${GITHUB_API}/repos/${repo}/readme`;

  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const options = {
      headers: {
        'User-Agent': 'material-fetcher',
        'Accept': 'application/vnd.github.v3+json'
      }
    };

    if (token) {
      options.headers['Authorization'] = `token ${token}`;
    }

    lib.get(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const readme = JSON.parse(data);

          // 检查是否有 content 字段
          if (!readme.content) {
            console.log('[GitHub Fetcher] README 无 content 字段');
            resolve([]);
            return;
          }

          const content = Buffer.from(readme.content, 'base64').toString('utf-8');

          // 提取 Markdown 图片链接 ![alt](url)
          const markdownImgRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
          const images = [];
          let match;

          while ((match = markdownImgRegex.exec(content)) !== null) {
            const imgUrl = match[2].startsWith('http')
              ? match[2]
              : `https://raw.githubusercontent.com/${repo}/main/${match[2]}`;
            images.push({
              alt: match[1],
              url: imgUrl
            });
          }

          console.log(`[GitHub Fetcher] README 中提取到 ${images.length} 张图片`);
          resolve(images);
        } catch (e) {
          console.error('[GitHub Fetcher] README 解析失败:', e.message);
          resolve([]); // 返回空数组而不是拒绝
        }
      });
    }).on('error', (err) => {
      console.error('[GitHub Fetcher] README 请求错误:', err.message);
      resolve([]); // 返回空数组而不是拒绝
    });
  });
}

/**
 * 获取 Releases Assets
 * @param {string} repo - 仓库名
 * @returns {Promise<Array>}
 */
async function fetchReleasesAssets(repo) {
  const url = `${GITHUB_API}/repos/${repo}/releases/latest`;

  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const options = {
      headers: {
        'User-Agent': 'material-fetcher',
        'Accept': 'application/vnd.github.v3+json'
      }
    };

    lib.get(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const release = JSON.parse(data);
          const assets = release.assets || [];
          resolve(assets.map(asset => ({
            name: asset.name,
            url: asset.browser_download_url,
            size: asset.size,
            content_type: asset.content_type
          })));
        } catch (e) {
          reject(new Error(`解析失败：${e.message}`));
        }
      });
    }).on('error', reject);
  });
}

/**
 * 主函数：获取 GitHub 仓库资源
 * @param {string} repo - 仓库名
 * @param {string} type - 类型：logo|screenshot|assets|all
 * @param {string} outputDir - 输出目录
 * @param {string} token - GitHub Token
 */
async function fetchGitHub(repo, type = 'all', outputDir, token = null) {
  const results = {
    repo,
    type,
    outputDir,
    files: [],
    errors: []
  };

  try {
    // 1. 获取文件列表
    const files = await fetchRepoFiles(repo, token);

    if (type === 'logo' || type === 'all') {
      // 识别 Logo 文件
      const logoFiles = identifyLogoFiles(files);

      for (const file of logoFiles) {
        const filename = `logo_${repo.replace('/', '_')}_${file.name}`;
        const result = await downloadFile(file.download_url, `${outputDir}/${filename}`);
        if (result.success) {
          results.files.push({ type: 'logo', path: result.path });
        } else {
          results.errors.push(`Logo 下载失败：${file.name}`);
        }
      }

      // 从 README 提取图片
      const readmeImages = await extractImagesFromReadme(repo, token);
      for (const img of readmeImages) {
        const filename = `readme_${repo.replace('/', '_')}_${Date.now()}.jpg`;
        const result = await downloadFile(img.url, `${outputDir}/${filename}`);
        if (result.success) {
          results.files.push({ type: 'readme_image', path: result.path, alt: img.alt });
        }
      }
    }

    if (type === 'assets' || type === 'all') {
      // 获取 Releases Assets
      const assets = await fetchReleasesAssets(repo);
      for (const asset of assets) {
        const filename = `asset_${asset.name}`;
        const result = await downloadFile(asset.url, `${outputDir}/${filename}`);
        if (result.success) {
          results.files.push({ type: 'asset', path: result.path, name: asset.name });
        }
      }
    }

  } catch (error) {
    results.errors.push(error.message);
  }

  return results;
}

module.exports = {
  fetchGitHub,
  fetchRepoFiles,
  identifyLogoFiles,
  extractImagesFromReadme,
  fetchReleasesAssets
};
