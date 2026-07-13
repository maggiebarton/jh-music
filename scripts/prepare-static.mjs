import { cp, mkdir, rm, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import sharp from "sharp";

const root = process.cwd();
const destination = resolve(root, "docs");

await rm(destination, { recursive: true, force: true });
await mkdir(destination, { recursive: true });
await writeFile(resolve(destination, ".nojekyll"), "");

for (const file of [
  "index.html",
  "style.css",
  "epk.css",
  "main.js",
  "favicon.ico",
  "CNAME",
  "tailwind.generated.css",
]) {
  await cp(resolve(root, file), resolve(destination, file));
}

for (const directory of ["epk", "output"]) {
  await cp(resolve(root, directory), resolve(destination, directory), { recursive: true });
}

const sourceImages = resolve(root, "images");
const deployedImages = resolve(destination, "images");
await mkdir(deployedImages, { recursive: true });

for (const asset of [
  "apple-touch-icon.png",
  "favicon-32.png",
  "favicon.png",
  "jh-logo-svg.svg",
]) {
  await cp(resolve(sourceImages, asset), resolve(deployedImages, asset));
}

for (const photo of ["jh-1.jpg", "jh-2.jpg", "jh-4.jpg", "jh-5.jpg", "jh-9.jpg"]) {
  await sharp(resolve(sourceImages, photo))
    .rotate()
    .resize({ width: 2400, height: 2400, fit: "inside", withoutEnlargement: true })
    .jpeg({ quality: 84, mozjpeg: true })
    .toFile(resolve(deployedImages, photo));
}
