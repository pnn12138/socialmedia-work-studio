/**
 * Image Finder 测试脚本
 *
 * 用法：
 * node test.js "搜索关键词" --orientation=landscape --per_page=5
 */

const finder = require('./index');

// 解析命令行参数
const args = process.argv.slice(2);

function parseArgs(args) {
  const result = {
    query: 'nature',
    options: {}
  };

  args.forEach(arg => {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      if (key === 'per_page' || key === 'page') {
        result.options[key] = parseInt(value, 10);
      } else {
        result.options[key] = value;
      }
    } else if (!result.query || result.query === 'nature') {
      result.query = arg;
    }
  });

  return result;
}

async function run() {
  const { query, options } = parseArgs(args);

  console.log(`\n🔍 Searching images for: "${query}"`);
  console.log(`Options:`, JSON.stringify(options, null, 2));
  console.log('\n');

  try {
    const results = await finder.searchImages(query, options);

    console.log('✅ Search Results:');
    console.log(`Source: ${results.source}`);
    console.log(`Query: ${results.query}`);
    console.log(`Found: ${results.results.length} images\n`);

    results.results.forEach((photo, index) => {
      console.log(`--- Image ${index + 1} ---`);
      console.log(`ID: ${photo.id}`);
      console.log(`Title: ${photo.title}`);
      console.log(`Photographer: ${photo.photographer}`);
      console.log(`Dimensions: ${photo.width}x${photo.height}`);
      console.log(`Image URL: ${photo.image_url}`);
      console.log(`Thumb URL: ${photo.thumb_url}`);
      console.log(`Page URL: ${photo.page_url}`);
      console.log('');
    });

    // 输出 Top 5 image URLs
    console.log('=== TOP 5 IMAGE URLs ===\n');
    results.results.slice(0, 5).forEach((photo, index) => {
      console.log(`${index + 1}. ${photo.image_url}`);
    });

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

run();
