/**
 * Logo Grabber - Logo 专用获取（聚合器）
 *
 * 从多渠道聚合搜索品牌 Logo，返回最佳候选
 */

const { fetchGitHub } = require('../fetchers/github-fetcher');
const { fetchWebAssets } = require('../fetchers/web-assets');
const { downloadFile } = require('../downloaders/universal');

/**
 * 构建品牌相关的 GitHub 搜索查询
 * @param {string} brandName - 品牌名
 * @returns {Array<string>}
 */
function buildGitHubQueries(brandName) {
  const queries = [];

  // 清理品牌名中的特殊字符
  const cleanName = brandName.toLowerCase().replace(/[^a-z0-9]/g, '');

  // 可能的仓库名组合
  queries.push(`${cleanName}/${cleanName}`);
  queries.push(`${cleanName}-org/${cleanName}`);
  queries.push(`${cleanName}hq/${cleanName}`);
  queries.push(`${cleanName}hq/${cleanName}-official`);
  queries.push(`${cleanName}official/${cleanName}`);

  return queries;
}

/**
 * 构建品牌官网 URL 猜测
 * @param {string} brandName - 品牌名
 * @returns {Array<string>}
 */
function buildWebQueries(brandName) {
  const queries = [];
  const cleanName = brandName.toLowerCase().replace(/[^a-z0-9]/g, '');

  // 常见域名模式
  queries.push(`https://${cleanName}.com`);
  queries.push(`https://${cleanName}.org`);
  queries.push(`https://${cleanName}.io`);
  queries.push(`https://${cleanName}hq.com`);
  queries.push(`https://${cleanName}official.com`);
  queries.push(`https://www.${cleanName}.com`);

  return queries;
}

/**
 * 主函数：聚合搜索 Logo
 * @param {string} brandName - 品牌名
 * @param {string} outputDir - 输出目录
 * @returns {Promise<Object>}
 */
async function fetchLogo(brandName, outputDir) {
  const results = {
    brandName,
    outputDir,
    files: [],
    sources: [],
    errors: []
  };

  console.log(`[Logo Grabber] 开始搜索品牌 "${brandName}" 的 Logo...`);

  // 1. GitHub 搜索
  console.log('[Logo Grabber] 搜索 GitHub...');
  const githubQueries = buildGitHubQueries(brandName);

  for (const query of githubQueries) {
    try {
      const ghResult = await fetchGitHub(query, 'logo', outputDir, process.env.GITHUB_TOKEN);
      if (ghResult.files.length > 0) {
        results.files.push(...ghResult.files);
        results.sources.push({ type: 'github', repo: query });
        console.log(`[Logo Grabber] GitHub "${query}" 找到 ${ghResult.files.length} 个 Logo`);
        break; // 找到后停止
      }
    } catch (error) {
      // 继续尝试下一个
    }
  }

  // 2. 官网搜索
  console.log('[Logo Grabber] 搜索官网...');
  const webQueries = buildWebQueries(brandName);

  for (const query of webQueries) {
    try {
      const webResult = await fetchWebAssets(query, 'logo', outputDir);
      if (webResult.files.length > 0) {
        results.files.push(...webResult.files);
        results.sources.push({ type: 'web', url: query });
        console.log(`[Logo Grabber] 官网 "${query}" 找到 ${webResult.files.length} 个 Logo`);
        break; // 找到后停止
      }
    } catch (error) {
      // 继续尝试下一个
    }
  }

  // 3. 去重和排序
  if (results.files.length > 0) {
    // 优先 SVG 格式
    results.files.sort((a, b) => {
      const aIsSvg = a.path.endsWith('.svg');
      const bIsSvg = b.path.endsWith('.svg');
      if (aIsSvg && !bIsSvg) return -1;
      if (!aIsSvg && bIsSvg) return 1;
      return 0;
    });
  }

  console.log(`[Logo Grabber] 完成，共找到 ${results.files.length} 个 Logo 候选`);

  return results;
}

module.exports = {
  fetchLogo,
  buildGitHubQueries,
  buildWebQueries
};
