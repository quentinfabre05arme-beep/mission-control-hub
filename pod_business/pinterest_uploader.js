/**
 * Pinterest Pin Creator
 * Generates pins for each product to drive traffic
 */

const products = [
  { title: 'Bitcoin Treasury', price: 29.99, tags: ['bitcoin', 'crypto', 'tshirt'] },
  { title: 'HODL Strong', price: 29.99, tags: ['hodl', 'bitcoin', 'crypto'] },
  { title: 'Fitness Motivation', price: 27.99, tags: ['fitness', 'gym', 'workout'] },
  { title: 'Professional Pride', price: 27.99, tags: ['professional', 'career'] },
  { title: 'Work Hard', price: 27.99, tags: ['motivation', 'success'] }
];

// Generate pin descriptions optimized for Pinterest SEO
function generatePinDesc(product) {
  const hashtags = product.tags.map(t => `#${t}`).join(' ');
  return `${product.title} — $${product.price}\nPremium quality tee perfect for ${product.tags.join(' lovers, ')} lovers!\n\nShop now: https://quentinvestdesigns.etsy.com\n\n${hashtags} #tshirt #fashion #gift`;
}

console.log('📌 Pinterest Pin Content');
console.log('════════════════════════\n');

products.forEach((p, i) => {
  console.log(`${i+1}. ${p.title}`);
  console.log('─────────────────────');
  console.log(generatePinDesc(p));
  console.log('\n');
});

console.log('💡 Next: Upload to Pinterest with product images');
console.log('🔗 Create account: https://business.pinterest.com');
