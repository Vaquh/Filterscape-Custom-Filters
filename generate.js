function normalizeBlock(text) {
  return text.replace(/\r\n/g, '\n')
             .replace(/\r/g, '\n')
             .replace(/^\n+/, '')
             .replace(/\s+$/, '');
}

async function buildModule(dir) {
  const files = [];

  for await (const entry of Deno.readDir(dir)) {
    if (entry.isFile && entry.name.endsWith('rs2f')) {
      files.push(`${dir}/${entry.name}`);
    }
  }
  
  files.sort();

  const module = await Promise.all(
    files.map(async (f) => normalizeBlock(await Deno.readTextFile(f)))
  );

  return module.join('\n'.repeat(2));
}

const filterMeta = {
  type: 'filter',
  name: 'vaquh/custom',
  description: 'Custom filter based on riktenx/filterscape',
  modules: [
    { moduleDir: 'module/general' },
    { moduleDir: 'module/junk' },
    { moduleDir: 'module/slayer' },
    { moduleDir: 'module/wildy' },
    { moduleDir: 'module/boss' },
    { moduleDir: 'module/cox' },
    { moduleDir: 'module/toa' },
    { moduleDir: 'module/shades' },
    { moduleDir: 'module/defender' },
    { moduleDir: 'module/unique' },
    { moduleDir: 'module/potion' },
    { moduleDir: 'module/clue' },
    { moduleDir: 'module/herb' },
    { moduleDir: 'module/currency' },
    { moduleDir: 'module/value' },
  ],
};

const filterHeader = normalizeBlock(`
/*@ define:module:header
hidden: true
name: header
*/
meta {
  name = "${filterMeta.name}";
  description = "${filterMeta.description}";
}
`);

const filterBody = (await Promise.all(
  filterMeta.modules.map((m) => buildModule(m.moduleDir))
)).join('\n'.repeat(4));

const filterFooter = normalizeBlock(`
`);

const filterSections = [
  filterHeader,
  filterBody,
  filterFooter,
].filter(section => section.trim().length > 0);

const assembledFilter = filterSections.join('\n'.repeat(6))
                                      + '\n'.repeat(1);

Deno.writeTextFileSync('vaquh_custom.rs2f', assembledFilter);
