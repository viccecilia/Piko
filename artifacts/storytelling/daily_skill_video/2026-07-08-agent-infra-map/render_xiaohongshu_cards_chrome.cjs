const fs = require("node:fs");
const fsp = require("node:fs/promises");
const path = require("node:path");
const { execFileSync } = require("node:child_process");
const { pathToFileURL } = require("node:url");

const root = __dirname;
const htmlPath = path.join(root, "xiaohongshu_cards.html");
const outputDir = path.join(root, "xiaohongshu", "cards");
const tempDir = path.join(root, "xiaohongshu", "_render_pages");
const chromePath = "C:/Program Files/Google/Chrome/Application/chrome.exe";

const filenames = [
  "P1_cover.png",
  "P2_old_pain.png",
  "P3_graphify.png",
  "P4_headroom.png",
  "P5_openrath.png",
  "P6_triggerdev.png",
  "P7_map.png",
  "P8_limits.png",
  "P9_checklist.png",
];

function standalonePage(style, cardHtml) {
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>${style}
    html, body { margin: 0 !important; width: 1080px !important; height: 1440px !important; overflow: hidden !important; background: #111 !important; }
    .card {
      width: 1080px !important;
      height: 1440px !important;
      aspect-ratio: auto !important;
      margin: 0 !important;
      border: 0 !important;
      box-shadow: none !important;
    }
  </style>
</head>
<body>${cardHtml}</body>
</html>`;
}

async function main() {
  if (!fs.existsSync(chromePath)) {
    throw new Error(`Chrome executable not found: ${chromePath}`);
  }

  const html = await fsp.readFile(htmlPath, "utf8");
  const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
  if (!styleMatch) throw new Error("Could not find <style> block in source HTML");

  const cardMatches = [...html.matchAll(/<section class="card(?: dark)?">[\s\S]*?<\/section>/g)];
  if (cardMatches.length !== filenames.length) {
    throw new Error(`Expected ${filenames.length} cards, found ${cardMatches.length}`);
  }

  await fsp.mkdir(outputDir, { recursive: true });
  await fsp.mkdir(tempDir, { recursive: true });

  for (let i = 0; i < filenames.length; i += 1) {
    const tempHtml = path.join(tempDir, `card_${i + 1}.html`);
    const outPng = path.join(outputDir, filenames[i]);
    await fsp.writeFile(tempHtml, standalonePage(styleMatch[1], cardMatches[i][0]), "utf8");

    execFileSync(chromePath, [
      "--headless=new",
      "--disable-gpu",
      "--hide-scrollbars",
      "--force-device-scale-factor=1",
      "--window-size=1080,1440",
      `--screenshot=${outPng}`,
      pathToFileURL(tempHtml).href,
    ], { stdio: "pipe" });
  }

  console.log(JSON.stringify({
    status: "RENDERED",
    renderer: "chrome-headless",
    outputDir,
    files: filenames,
  }, null, 2));
}

main().catch((error) => {
  console.error("RENDER_FAILED");
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
