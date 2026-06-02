const filterMeta = {
  type: 'filter',
  name: 'vaquh/custom',
  description: 'Custom filter based on riktenx/filterscape',
  modules: [
    { modulePath: 'module/general/module.rs2f' },
    { modulePath: 'module/junk/module.rs2f' },
    { modulePath: 'module/slayer/module.rs2f' },
    { modulePath: 'module/wildy/module.rs2f' },
    { modulePath: 'module/boss/module.rs2f' },
    { modulePath: 'module/cox/module.rs2f' },
    { modulePath: 'module/toa/module.rs2f' },
    { modulePath: 'module/shades/module.rs2f' },
    { modulePath: 'module/defender/module.rs2f' },
    { modulePath: 'module/unique/module.rs2f' },
    { modulePath: 'module/potion/module.rs2f' },
    { modulePath: 'module/clue/module.rs2f' },
    { modulePath: 'module/herb/module.rs2f' },
    { modulePath: 'module/currency/module.rs2f' },
    { modulePath: 'module/value/module.rs2f' },
  ],
};

const filterHeader = `
/*@ define:module:header
hidden: true
name: header
*/
meta {
  name = "${filterMeta.name}";
  description = "${filterMeta.description}";
}
`;

function normalizeBlock(text) {
  return text.replace(/\r\n/g, '\n')
             .replace(/\r/g, '\n')
             .replace(/^\n+/, '')
             .replace(/\s+$/, '');
}

const assembledFilter = [
  normalizeBlock(filterHeader),
  filterMeta.modules.map((module) => {
    return normalizeBlock(Deno.readTextFileSync(module.modulePath));
  })
    .join('\n'.repeat(4)),
]
  .join('\n'.repeat(6))
  + '\n'.repeat(2);

Deno.writeTextFileSync('vaquh_custom.rs2f', assembledFilter);
