export function GET() {
  const site = import.meta.env.SITE || 'https://chinamanufacturingintel.example/';
  const body = `User-agent: *
Allow: /

Sitemap: ${new URL('/sitemap.xml', site).toString()}
`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
