import type { Entity, Kind } from './entities';
import { entityUrl, fmtDate, KIND_LABEL } from './entities';

export const SITE_NAME = 'China Manufacturing Intelligence';
export const SITE_TAGLINE =
  'A sourced English-language knowledge base for China\u2019s manufacturing geography, industrial clusters, products, and supply chains.';

export interface JsonLdNode {
  '@type': string;
  [k: string]: unknown;
}

export function orgJsonLd(site: URL): JsonLdNode {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: SITE_NAME,
    url: site.origin + '/',
    description:
      'Independent editorial knowledge base on China manufacturing clusters, cities, industries, and products.',
  };
}

export function webSiteJsonLd(site: URL): JsonLdNode {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: SITE_NAME,
    url: site.origin + '/',
    inLanguage: 'en',
    publisher: { '@type': 'Organization', name: SITE_NAME, url: site.origin + '/' },
  };
}

export function articleJsonLd(site: URL, e: Entity): JsonLdNode {
  const url = new URL(entityUrl(e), site).toString();
  const d = e.entry.data as any;
  const published = fmtDate(d.date);
  const modified = fmtDate(d.last_verified) || published;

  // articleSection: super_sector for industries, else product industry, else kind label.
  let section: string | undefined;
  if (e.kind === 'industry' && typeof d.super_sector === 'string' && d.super_sector) {
    section = d.super_sector;
  } else if (e.kind === 'product' && typeof d.industry === 'string' && d.industry) {
    section = d.industry;
  } else {
    section = KIND_LABEL[e.kind];
  }

  const node: JsonLdNode = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: e.title,
    description: e.description,
    url,
    mainEntityOfPage: url,
    inLanguage: 'en',
    isAccessibleForFree: true,
    author: { '@type': 'Organization', name: SITE_NAME, url: site.origin + '/' },
    publisher: { '@type': 'Organization', name: SITE_NAME, url: site.origin + '/' },
  };
  if (section) node.articleSection = section;
  const body = (e.entry as any).body as string | undefined;
  if (body) {
    const wc = body.trim().split(/\s+/).length;
    if (wc > 0) node.wordCount = wc;
  }
  if (published) node.datePublished = published;
  if (modified) node.dateModified = modified;
  return node;
}

export function breadcrumbJsonLd(site: URL, items: { name: string; url: string }[]): JsonLdNode {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((it, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: it.name,
      item: new URL(it.url, site).toString(),
    })),
  };
}
