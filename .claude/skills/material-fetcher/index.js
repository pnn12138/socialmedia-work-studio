/**
 * Material Fetcher - 素材获取模块主入口
 *
 * 统一命令行接口，协调各 Fetcher 执行任务
 */

const path = require('path');
const fs = require('fs');
const { fetchGitHub } = require('./fetchers/github-fetcher');
const { fetchWebAssets } = require('./fetchers/web-assets');
const { fetchLogo } = require('./fetchers/logo-grabber');

/**
 * 解析用户输入的命令
 * @param {string} input - 用户输入
 * @returns {Object}
 */
function parseCommand(input) {
  const parts = input.trim().split(/\s+/);
  const command = parts[0];
  const options = {};

  // 解析 type 参数
  const typeMatch = input.match(/type:(\w+)/);
  if (typeMatch) {
    options.type = typeMatch[1];
  }

  // 解析 output 参数（支持带引号的路径）
  const outputMatch = input.match(/output:("([^"]+)"|'([^']+)'|([^\s]+))/);
  if (outputMatch) {
    options.output = outputMatch[2] || outputMatch[3] || outputMatch[4];
  }

  // 解析源和标识符
  let source, identifier;

  if (command.startsWith('github:')) {
    source = 'github';
    identifier = command.slice(7);
  } else if (command.startsWith('web:')) {
    source = 'web';
    identifier = command.slice(4);
  } else if (command.startsWith('xhs:')) {
    source = 'xhs';
    identifier = command.slice(4);
  } else if (command.startsWith('logo:')) {
    source = 'logo';
    identifier = command.slice(5);
  } else if (parts.length >= 2) {
    // 兼容格式：material-fetcher github user/repo
    source = parts[1];
    identifier = parts[2];
  }

  return { source, identifier, options };
}

/**
 * 获取默认输出目录
 * @returns {string}
 */
function getDefaultOutputDir() {
  // 尝试查找当前项目的 fig/素材 目录
  const cwd = process.cwd();
  const possiblePaths = [
    path.join(cwd, 'fig', '素材'),
    path.join(cwd, 'fig', 'material'),
    path.join(cwd, 'material-fetcher', 'output')
  ];

  for (const p of possiblePaths) {
    if (fs.existsSync(path.dirname(p))) {
      if (!fs.existsSync(p)) {
        fs.mkdirSync(p, { recursive: true });
      }
      return p;
    }
  }

  // 默认返回 module 下的 output 目录
  const defaultPath = path.join(__dirname, 'output');
  if (!fs.existsSync(defaultPath)) {
    fs.mkdirSync(defaultPath, { recursive: true });
  }
  return defaultPath;
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2).join(' ');

  if (!args || args === '-h' || args === '--help') {
    console.log(`
Material Fetcher - 素材获取模块

用法:
  node index.js <source>:<identifier> [type:<类型>] [output:<路径>]

支持的源:
  github:<user/repo>  - GitHub 仓库
  web:<url>           - 官网 URL
  xhs:<feed_id>       - 小红书笔记 ID
  logo:<brand_name>   - 品牌名（聚合搜索）

type 参数:
  logo      - 仅获取 Logo
  screenshot - 仅截图
  assets    - 仅获取 Assets
  all       - 获取全部（默认）

示例:
  node index.js github:petersteinberger/openclaw type:logo
  node index.js web:https://example.com type:all
  node index.js logo:OpenClaw
`);
    process.exit(0);
  }

  const { source, identifier, options } = parseCommand(args);
  const outputDir = options.output || getDefaultOutputDir();

  if (!source || !identifier) {
    console.error('错误：无法解析源和标识符');
    console.log('使用 -h 查看帮助');
    process.exit(1);
  }

  console.log(`\n[Material Fetcher] 开始获取...`);
  console.log(`  源：${source}`);
  console.log(`  标识符：${identifier}`);
  console.log(`  输出目录：${outputDir}\n`);

  let result;

  try {
    switch (source) {
      case 'github':
        result = await fetchGitHub(identifier, options.type || 'all', outputDir);
        break;

      case 'web':
        result = await fetchWebAssets(identifier, options.type || 'all', outputDir);
        break;

      case 'logo':
        result = await fetchLogo(identifier, outputDir);
        break;

      case 'xhs':
        console.log('[Material Fetcher] 小红书下载功能需要扩展 xiaohongshu-mcp 服务');
        console.log('请参考 CLAUDE.md 中的实现指南');
        process.exit(1);
        break;

      default:
        console.error(`错误：未知的源 "${source}"`);
        process.exit(1);
    }

    // 输出结果
    console.log('\n[Material Fetcher] 获取完成！\n');

    if (result.files && result.files.length > 0) {
      console.log('获取到的文件：');
      result.files.forEach((file, i) => {
        console.log(`  ${i + 1}. [${file.type}] ${path.basename(file.path)}`);
        console.log(`     路径：${file.path}`);
      });
    } else {
      console.log('未找到符合条件的素材。');
    }

    if (result.errors && result.errors.length > 0) {
      console.log('\n错误：');
      result.errors.forEach((err, i) => {
        console.log(`  ${i + 1}. ${err}`);
      });
    }

    console.log('');

  } catch (error) {
    console.error('[Material Fetcher] 执行失败:', error.message);
    process.exit(1);
  }
}

// 如果是直接执行
if (require.main === module) {
  main();
}

module.exports = {
  parseCommand,
  getDefaultOutputDir,
  main
};
