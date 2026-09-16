import { getEntityIndex, entityUrl, KIND_ROUTE, type Kind } from '../lib/entities';

export async function GET() {
  const index = await getEntityIndex();
  const site = import.meta.env.SITE || 'https://chinamanufacturingintel.example/';

  const staticPaths = ['/', '/about/', '/methodology/'];

  const urls: { loc: string }[] = [];

  for (const p of staticPaths) {
    urls.push({ loc: new URL(p, site).toString() });
  }
  for (const kind of Object.keys(KIND_ROUTE) as Kind[]) {
    urls.push({ loc: new URL(KIND_ROUTE[kind], site).toString() });
  }
  for (const e of index.all) {
    urls.push({ loc: new URL(entityUrl(e), site).toString() });
  }

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((u) => `  <url><loc>${u.loc}</loc></url>`).join('\n')}
</urlset>
`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
}
