// Checks dashboard logic with a minimal DOM stub; not a visual browser test.
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
let code = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes = new Map();
function element() { return { style:{}, value:'10', textContent:'', innerHTML:'', classList:{add(){}}, setAttribute(){}, append(){}, replaceChildren(){}, addEventListener(){}, querySelector(){return element();} }; }
const document = {getElementById(id){if(id==='embedded-portfolio')return null;if(!nodes.has(id))nodes.set(id,element());return nodes.get(id);},createElement:element,createElementNS:element};
code = code.replace(/\}\)\(\);\s*$/, 'globalThis.api={extract,parseCSV,load(rows){loaded=extract(rows);population={n:loaded.length,defaults:loaded.reduce((s,r)=>s+r.default,0),avgLimit:loaded.reduce((s,r)=>s+r.limit,0)/loaded.length};updateKPIs();}};})();');
const context = {document,console,innerWidth:1400};vm.createContext(context);vm.runInContext(code,context);
const {api}=context;
assert.equal(nodes.get('stressedRate').textContent,'24.33%');
assert.equal(nodes.get('stressedCount').textContent,'7,300');
const row={ID:'1',LIMIT_BAL:'50000',PAY_0:'0',AGE:'25','default.payment.next.month':'1'};
for(const key of ['ID','LIMIT_BAL','PAY_0','AGE','default.payment.next.month']) {
 for(const value of ['', ' ', null, 'Infinity']) assert.throws(()=>api.extract([{...row,[key]:value}]));
}
assert.throws(()=>api.extract([row,row]));
assert.throws(()=>api.extract([{...row,X1:50000}]));
assert.throws(()=>api.extract([]));
assert.throws(()=>api.parseCSV('a,b\n1,2,3'));
assert.throws(()=>api.parseCSV('a,b\n"1,2'));
assert.throws(()=>api.parseCSV('a,a\n1,2'));
assert.equal(api.parseCSV('a,b\n"hello\nworld",2')[0].a,'hello\nworld');
assert.equal(api.parseCSV('\uFEFFa,b\r\n"one, two",3')[0].a,'one, two');
api.load([row,{...row,ID:'2','default.payment.next.month':'0'}]);
assert.equal(nodes.get('kpiClients').textContent,'2');
assert.equal(nodes.get('stressPopulation').textContent,'2');
assert.equal(nodes.get('insightRate').textContent,'50.00%');
assert.equal(nodes.get('stressedRate').textContent,'55.00%');
console.log('Dashboard checks passed: initial metrics, CSV validation, duplicates, quoted fields and dynamic population text.');
