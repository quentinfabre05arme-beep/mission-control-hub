const fs = require('fs');
const path = require('path');

const inputFile = process.argv[2] || 'generated/design_1_output.json';
const outputFile = process.argv[3] || 'generated/design_1_bitcoin_millionaire.png';

console.log(`Extracting image from: ${inputFile}`);
console.log(`Saving to: ${outputFile}`);

try {
  // Read file as UTF-16LE (Windows PowerShell default)
  const raw = fs.readFileSync(inputFile);
  
  // Handle BOM and convert
  let content;
  if (raw.length >= 2 && raw[0] === 0xFF && raw[1] === 0xFE) {
    // UTF-16LE with BOM
    content = raw.slice(2).toString('utf16le');
  } else if (raw.length >= 2 && raw[0] === 0xFE && raw[1] === 0xFF) {
    // UTF-16BE with BOM
    content = raw.slice(2).toString('utf16be');
  } else if (raw.length >= 3 && raw[0] === 0xEF && raw[1] === 0xBB && raw[2] === 0xBF) {
    // UTF-8 with BOM
    content = raw.slice(3).toString('utf8');
  } else {
    content = raw.toString('utf8');
  }
  
  // Parse JSON
  const data = JSON.parse(content);
  
  console.log('Response structure:', Object.keys(data));
  if (data.data) console.log('Data structure:', Object.keys(data.data));
  if (data.data?.data) console.log('Nested data structure:', Object.keys(data.data.data));
  
  let base64 = null;
  
  if (data.data?.b64_json) {
    base64 = data.data.b64_json;
  } else if (data.data?.data?.b64_json) {
    base64 = data.data.data.b64_json;
  } else if (Array.isArray(data.data) && data.data[0]?.b64_json) {
    base64 = data.data[0].b64_json;
  } else if (data.data?.data && Array.isArray(data.data.data) && data.data.data[0]?.b64_json) {
    base64 = data.data.data[0].b64_json;
  }
  
  if (base64) {
    const imageBuffer = Buffer.from(base64, 'base64');
    fs.writeFileSync(outputFile, imageBuffer);
    console.log(`✅ Image extracted successfully!`);
    console.log(`Size: ${(imageBuffer.length / 1024).toFixed(2)} KB`);
  } else {
    console.log('❌ No image data found in response');
    console.log('Data sample:', JSON.stringify(data.data).slice(0, 500));
  }
} catch (err) {
  console.error('❌ Error:', err.message);
}
