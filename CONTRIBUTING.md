# Contributing to TOP

This file contains instructions for humans and AI agents working with this repository.

---

## For AI agents

If the user asks to set up GitHub validation for this repository, follow the steps below.

### Setting up GitHub Actions validation

Create the following two files in the repository:

**1. `.github/workflows/validate-skill.yml`**

```yaml
name: validate-skill

on:
  pull_request:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Validate JSON files
        run: node scripts/validate-json.mjs

      - name: Validate manifest links
        run: node scripts/validate-manifest-links.mjs

      - name: Validate prompt references
        run: node scripts/validate-prompt-references.mjs

      - name: Validate license consistency
        run: node scripts/validate-license.mjs
```

**2. `scripts/validate-json.mjs`** — checks all `*.json` files parse without errors:

```js
import { readFileSync } from 'fs';
import { globSync } from 'fs';
import path from 'path';

const files = globSync('top-skill/**/*.json');
let errors = 0;

for (const file of files) {
  try {
    JSON.parse(readFileSync(file, 'utf8'));
  } catch (e) {
    console.error(`Invalid JSON: ${file}\n  ${e.message}`);
    errors++;
  }
}

if (errors > 0) process.exit(1);
console.log(`✓ ${files.length} JSON files valid`);
```

**3. `scripts/validate-manifest-links.mjs`** — checks all paths in `skill.json` exist:

```js
import { readFileSync, existsSync } from 'fs';

const manifest = JSON.parse(readFileSync('top-skill/skill.json', 'utf8'));
const base = 'top-skill';
let errors = 0;

const checkPath = (p) => {
  const full = `${base}/${p}`;
  if (!existsSync(full)) {
    console.error(`Missing: ${full}`);
    errors++;
  }
};

checkPath(manifest.entrypoint);
checkPath(manifest.ai_preload);
checkPath(manifest.onboarding);
checkPath(manifest.changelog);
for (const f of [...manifest.agents, ...manifest.canon, ...manifest.examples]) {
  checkPath(f);
}

if (errors > 0) process.exit(1);
console.log(`✓ All manifest links exist`);
```

**4. `scripts/validate-prompt-references.mjs`** — checks that every `prompt` field in JSON specs points to an existing file:

```js
import { readFileSync, existsSync } from 'fs';
import { globSync } from 'fs';
import path from 'path';

const files = globSync('top-skill/examples/**/*.json');
let errors = 0;

for (const file of files) {
  const dir = path.dirname(file);
  let tree;
  try { tree = JSON.parse(readFileSync(file, 'utf8')); } catch { continue; }

  const check = (node) => {
    if (node.prompt) {
      const full = path.join(dir, node.prompt);
      if (!existsSync(full)) {
        console.error(`Missing prompt: ${full} (referenced in ${file})`);
        errors++;
      }
    }
    for (const child of node.children || []) check(child);
  };
  check(tree);
}

if (errors > 0) process.exit(1);
console.log(`✓ All prompt references valid`);
```

**5. `scripts/validate-license.mjs`** — checks license and email are consistent:

```js
import { readFileSync } from 'fs';

const manifest = JSON.parse(readFileSync('top-skill/skill.json', 'utf8'));
const license = readFileSync('top-skill/LICENSE.md', 'utf8');
let errors = 0;

if (manifest.license !== 'MIT') {
  console.error(`skill.json license is "${manifest.license}", expected "MIT"`);
  errors++;
}
if (!license.includes(manifest.author.email)) {
  console.error(`LICENSE.md does not contain email "${manifest.author.email}"`);
  errors++;
}

if (errors > 0) process.exit(1);
console.log(`✓ License consistent`);
```

---

## Metadata rules when making changes

When modifying any file inside `top-skill/`:

1. Update `top-skill/SKILL.md` → `**Last updated:**` field to today's date
2. Add an entry to `top-skill/CHANGELOG.md` under a new version
3. Bump `version` in `top-skill/skill.json` (patch version for fixes, minor for new features)

---

## Commit message format

```
type(scope): short description

Examples:
fix(onboarding): remove stale license gate
feat(agents): add domain-structuring execution steps
docs(readme): update getting started section
ci(validate): add json and reference validation workflow
```
