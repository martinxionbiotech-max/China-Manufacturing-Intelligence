import { getCollection } from 'astro:content';
import type { CollectionEntry } from 'astro:content';

export type Kind = 'cluster' | 'product' | 'industry' | 'city';

// Map collection name -> entity kind
export const COLLECTION_KIND: Record<string, Kind> = {
  clusters: 'cluster',
  products: 'product',
  industries: 'industry',
  cities: 'city',
};

// URL prefix per kind (matches phase roadmap routes)
export const KIND_ROUTE: Record<Kind, string> = {
  cluster: '/manufacturing-clusters/',
  product: '/products/',
  industry: '/industries/',
  city: '/manufacturing-cities/',
};

// Human labels
export const KIND_LABEL: Record<Kind, string> = {
  cluster: 'Manufacturing Cluster',
  product: 'Product',
  industry: 'Industry',
  city: 'Manufacturing City',
};
export const KIND_LABEL_PLURAL: Record<Kind, string> = {
  cluster: 'Manufacturing Clusters',
  product: 'Products',
  industry: 'Industries',
  city: 'Manufacturing Cities',
};

export interface Entity {
  id: string; // entity_id e.g. cls-ningde-power-battery
  kind: Kind;
  slug: string;
  title: string;
  description: string;
  entry: CollectionEntry<'clusters' | 'products' | 'industries' | 'cities'>;
}

export interface EntityIndex {
  byId: Map<string, Entity>;
  bySlug: Map<string, Entity>; // key: `${kind}:${slug}`
  all: Entity[];
  byKind: Record<Kind, Entity[]>;
}

let cache: EntityIndex | null = null;

export async function getEntityIndex(): Promise<EntityIndex> {
  if (cache) return cache;

  const [clusters, products, industries, cities] = await Promise.all([
    getCollection('clusters'),
    getCollection('products'),
    getCollection('industries'),
    getCollection('cities'),
  ]);

  const byId = new Map<string, Entity>();
  const bySlug = new Map<string, Entity>();
  const all: Entity[] = [];
  const byKind: Record<Kind, Entity[]> = { cluster: [], product: [], industry: [], city: [] };

  const push = (
    kind: Kind,
    entry: CollectionEntry<'clusters' | 'products' | 'industries' | 'cities'>,
  ) => {
    const d = entry.data as any;
    const e: Entity = {
      id: d.entity_id,
      kind,
      slug: d.slug,
      title: d.title,
      description: d.description,
      entry,
    };
    byId.set(e.id, e);
    bySlug.set(`${kind}:${e.slug}`, e);
    byKind[kind].push(e);
    all.push(e);
  };

  clusters.forEach((e) => push('cluster', e));
  products.forEach((e) => push('product', e));
  industries.forEach((e) => push('industry', e));
  cities.forEach((e) => push('city', e));

  const sortTitle = (a: Entity, b: Entity) => a.title.localeCompare(b.title);
  byKind.cluster.sort(sortTitle);
  byKind.product.sort(sortTitle);
  byKind.industry.sort(sortTitle);
  byKind.city.sort(sortTitle);

  cache = { byId, bySlug, all, byKind };
  return cache;
}

export function entityUrl(e: { kind: Kind; slug: string }): string {
  return `${KIND_ROUTE[e.kind]}${e.slug}/`;
}

/**
 * Resolve an entity_id (e.g. `cls-ningde-power-battery`) or a kind-scoped slug
 * reference to an Entity. Returns undefined when unresolvable (never fabricate).
 */
export function resolveRef(
  index: EntityIndex,
  kind: Kind,
  ref: string,
): Entity | undefined {
  if (!ref) return undefined;
  // exact entity_id
  if (index.byId.has(ref)) return index.byId.get(ref);
  // slug within a kind
  return index.bySlug.get(`${kind}:${ref}`);
}

/**
 * Resolve a free-text `related` URL (already a full path) to an Entity by
 * matching its route prefix + slug. Returns undefined if no page exists.
 */
export function resolveRelatedUrl(index: EntityIndex, url: string): Entity | undefined {
  if (!url) return undefined;
  let u = url.trim();
  // normalize trailing slash
  u = u.replace(/\/+$/, '') + '/';
  for (const kind of Object.keys(KIND_ROUTE) as Kind[]) {
    const prefix = KIND_ROUTE[kind];
    if (u.startsWith(prefix)) {
      const slug = u.slice(prefix.length).replace(/\/+$/, '');
      return index.bySlug.get(`${kind}:${slug}`);
    }
  }
  return undefined;
}

/**
 * Collect cross-links for an entity from (a) its structured reference fields and
 * (b) its `related` frontmatter list. Deduped, excludes self, never fabricates.
 */
export function crossLinks(
  index: EntityIndex,
  e: Entity,
): { cluster: Entity[]; product: Entity[]; industry: Entity[]; city: Entity[] } {
  const out: Record<Kind, Map<string, Entity>> = {
    cluster: new Map(),
    product: new Map(),
    industry: new Map(),
    city: new Map(),
  };
  const d = e.entry.data as any;

  const add = (target?: Entity) => {
    if (!target || target.id === e.id) return;
    out[target.kind].set(target.id, target);
  };

  // structured fields
  const majorClusters: string[] = Array.isArray(d.major_clusters) ? d.major_clusters : [];
  const majorProducts: string[] = Array.isArray(d.major_products) ? d.major_products : [];
  const majorIndustries: string[] = Array.isArray(d.major_industries) ? d.major_industries : [];
  const majorCities: string[] = Array.isArray(d.major_cities) ? d.major_cities : [];
  const industries: string[] = Array.isArray(d.industries) ? d.industries : [];
  const products: string[] = Array.isArray(d.products) ? d.products : [];

  for (const ref of majorClusters) add(resolveRef(index, 'cluster', ref));
  for (const ref of majorProducts) add(resolveRef(index, 'product', ref));
  for (const ref of majorIndustries) add(resolveRef(index, 'industry', ref));
  for (const ref of majorCities) add(resolveRef(index, 'city', ref));

  // single-valued refs
  if (typeof d.city === 'string') add(resolveRef(index, 'city', d.city));
  if (typeof d.industry === 'string') add(resolveRef(index, 'industry', d.industry));
  for (const ref of industries) add(resolveRef(index, 'industry', ref));
  for (const ref of products) add(resolveRef(index, 'product', ref));

  // free-text related URLs
  const related: string[] = Array.isArray(d.related) ? d.related : [];
  for (const url of related) add(resolveRelatedUrl(index, url));

  return {
    cluster: [...out.cluster.values()].sort((a, b) => a.title.localeCompare(b.title)),
    product: [...out.product.values()].sort((a, b) => a.title.localeCompare(b.title)),
    industry: [...out.industry.values()].sort((a, b) => a.title.localeCompare(b.title)),
    city: [...out.city.values()].sort((a, b) => a.title.localeCompare(b.title)),
  };
}

/** Human-readable date (YYYY-MM-DD) from string or Date. */
export function fmtDate(v: string | Date | undefined): string | undefined {
  if (!v) return undefined;
  if (v instanceof Date) {
    const d = v;
    return Number.isNaN(d.getTime())
      ? undefined
      : `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  }
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(v));
  return m ? m[0] : undefined;
}
