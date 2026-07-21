#!/usr/bin/env node
/**
 * AI Design Prompts for Grok Pro / Gemini Pro
 * Optimized for your existing tools
 */

const DESIGNS = [
  {
    title: "Crypto Millionaire",
    grokPrompt: `Create a bold, minimalist t-shirt design with the text "CRYPTO MILLIONAIRE" in a sleek, modern font. Add subtle Bitcoin/ethereum coin icons as background elements. Use black background with gold/white text. Style: Premium, luxury, clean. Vector-ready for print.`,
    geminiPrompt: `Design a premium t-shirt graphic featuring "CRYPTO MILLIONAIRE" in elegant typography. Include stylized cryptocurrency symbols (Bitcoin, Ethereum) as decorative elements. Color scheme: black, gold, white. High contrast, print-ready vector style.`,
    style: "Luxury, minimal"
  },
  {
    title: "Gym Beast Mode",
    grokPrompt: `Create an aggressive fitness t-shirt design with "BEAST MODE ACTIVATED" text. Use bold, blocky typography with distressed texture. Add subtle barbell/silhouette elements. Colors: Dark red, black, white. Energy: Powerful, intense. Print-ready.`,
    geminiPrompt: `Design a motivational gym t-shirt with "BEAST MODE ACTIVATED" in bold, impactful letters. Include fitness imagery (barbell, muscle silhouette) as background. Dark red and black color scheme. Gritty, powerful aesthetic. Vector format.`,
    style: "Aggressive, bold"
  },
  {
    title: "Startup Life",
    grokPrompt: `Create a tech startup t-shirt design featuring "STARTUP LIFE" and "COFFEE → CODE → REPEAT" text. Modern sans-serif fonts. Add subtle laptop/code elements. Colors: Navy blue, white, light blue. Clean, professional, startup culture vibe.`,
    geminiPrompt: `Design a startup culture t-shirt with "STARTUP LIFE" and "COFFEE → CODE → REPEAT" tagline. Include minimalist tech icons (laptop, coffee, code brackets). Navy blue and white color palette. Professional, modern aesthetic. Print-ready.`,
    style: "Tech, modern"
  },
  {
    title: "Code & Coffee",
    grokPrompt: `Create a developer t-shirt with "CODE & COFFEE" in elegant typography. Add coffee cup and code brackets/terminal symbols as decorative elements. Warm brown, cream, dark gray colors. Cozy programmer aesthetic. High quality print design.`,
    geminiPrompt: `Design a programmer lifestyle t-shirt featuring "CODE & COFFEE THE PERFECT STACK". Include coffee cup, code brackets, laptop imagery. Warm color palette: brown, cream, charcoal. Comfortable, relatable developer aesthetic. Vector format.`,
    style: "Cozy, relatable"
  },
  {
    title: "Hustle & Grind",
    grokPrompt: `Create a motivational t-shirt design with "HUSTLE & GRIND" in bold industrial typography. Add subtle success/arrow elements. Green, black, white colors. Success-oriented, entrepreneurial energy. Clean, powerful design.`,
    geminiPrompt: `Design an entrepreneurial t-shirt featuring "HUSTLE & GRIND SUCCESS IS THE ONLY OPTION". Use strong, industrial typography. Include subtle upward arrow/mountain elements. Green, black, white color scheme. Motivational, powerful aesthetic. Print-ready.`,
    style: "Motivational, bold"
  }
];

console.log('🎨 AI Design Prompts\n');
console.log('═══════════════════════════════════════════════════\n');

DESIGNS.forEach((design, i) => {
  console.log(`${i + 1}. ${design.title} (${design.style})`);
  console.log('─'.repeat(50));
  console.log('\n🦾 GROK PRO PROMPT:');
  console.log(design.grokPrompt);
  console.log('\n✨ GEMINI PRO PROMPT:');
  console.log(design.geminiPrompt);
  console.log('\n');
});

console.log('═══════════════════════════════════════════════════\n');
console.log('💡 USAGE:');
console.log('   1. Copy Grok prompt → chat.grok.com');
console.log('   2. Or copy Gemini prompt → gemini.google.com');
console.log('   3. Request: "High quality PNG, transparent background"');
console.log('   4. Download image, upload to Printify');
console.log('\n⚡ TIP: Grok tends to be more direct/follows instructions better');
console.log('⚡ TIP: Gemini often adds more creative flourishes');
console.log('');
