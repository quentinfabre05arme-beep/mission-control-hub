const token = process.env.PRINTIFY_API_KEY;
const parts = token.split('.');
const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString());

console.log('Token Analysis:');
console.log('Issued:', new Date(payload.iat * 1000).toISOString());
console.log('Expires:', new Date(payload.exp * 1000).toISOString());
console.log('Now:', new Date().toISOString());
console.log('Expired:', Date.now() > payload.exp * 1000);
console.log('Subject:', payload.sub);
console.log('Scopes:', payload.scopes);
console.log('');
console.log('If still getting 401, the token may be:');
console.log('1. Revoked by Printify');
console.log('2. IP-restricted');
console.log('3. Account-level blocked');
console.log('');
console.log('Next step: Generate fresh token from printify.com/app/account/api');
