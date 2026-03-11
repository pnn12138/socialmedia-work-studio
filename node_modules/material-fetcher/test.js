/**
 * 测试脚本：获取 OpenClaw Logo
 */

const { fetchGitHub } = require('./fetchers/github-fetcher');

async function test() {
  console.log('测试：获取 OpenClaw Logo\n');

  const outputDir = 'D:/social-work-flow/work-studio/02_内容项目/审稿中/OpenClaw 安全性分析/fig/素材';

  try {
    const result = await fetchGitHub(
      'petersteinberger/openclaw',
      'logo',
      outputDir,
      process.env.GITHUB_TOKEN
    );

    console.log('\n结果：');
    console.log(JSON.stringify(result, null, 2));

  } catch (error) {
    console.error('错误:', error.message);
  }
}

test();
