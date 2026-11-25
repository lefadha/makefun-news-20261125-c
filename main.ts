// Wednesday 25 November 2026, one page: 48 dated stories, a drawn scene in every
// card. render.py draws and commits entry.png; this program is what the sandbox
// runs, and it refuses to run rather than ship a file the gate would reject.
//
//   MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const CAP = 1_048_576;
const SIG = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function insist(ok: boolean, why: string): void {
  if (!ok) throw new Error(why);
}

const source = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(source);

insist(bytes.length <= CAP, `entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
SIG.forEach((v, i) => insist(bytes[i] === v, 'entry.png is not a PNG'));
insist(bytes.readUInt32BE(8) === 13 && bytes.toString('ascii', 12, 16) === 'IHDR',
  'the first PNG chunk is not IHDR');
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
const bitDepth = bytes[24];
const colourType = bytes[25];
insist(width === 1024 && height === 1024, `entry.png is ${width}x${height}, not 1024x1024`);
insist(bitDepth === 8, `bit depth ${bitDepth}, expected 8`);
insist(colourType === 2, `colour type ${colourType}, expected truecolour (2)`);

// the image must carry the page and not a blank: a 1 MiB cap and 1024 square are
// not enough on their own, so the length of the encoded stream is checked too
insist(bytes.length > 60_000, `entry.png is only ${bytes.length} bytes: too empty to be a page`);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
writeFileSync(target, bytes);

const back = readFileSync(target);
insist(back.length === bytes.length, 'the written file is a different length');
for (let i = 0; i < bytes.length; i += 4096) {
  const end = Math.min(i + 4096, bytes.length);
  insist(back.subarray(i, end).equals(bytes.subarray(i, end)), `the written file differs at byte ${i}`);
}

// the committed drawing is derived from the story list, so state the count the page
// claims where a reader of this file can see it
console.log(`wrote ${target}: ${bytes.length} bytes, ${width}x${height}, 48 stories, 8 regions`);
