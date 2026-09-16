import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const dateish = z.union([z.date(), z.string()]).optional();

const clusters = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../content/manufacturing-clusters' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    entity_id: z.string(),
    type: z.string(),
    slug: z.string(),
    status: z.string().optional(),
    date: dateish,
    last_verified: dateish,
    city: z.string().optional(),
    province: z.string().optional(),
    industries: z.array(z.string()).default([]),
    products: z.array(z.string()).default([]),
    related: z.array(z.string()).default([]),
  }),
});

const products = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../content/products' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    entity_id: z.string(),
    type: z.string(),
    slug: z.string(),
    status: z.string().optional(),
    date: dateish,
    last_verified: dateish,
    industry: z.string().optional(),
    hs_codes: z.array(z.string()).default([]),
    major_clusters: z.array(z.string()).default([]),
    major_cities: z.array(z.string()).default([]),
    related: z.array(z.string()).default([]),
  }),
});

const industries = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../content/industries' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    entity_id: z.string(),
    type: z.string(),
    slug: z.string(),
    status: z.string().optional(),
    date: dateish,
    last_verified: dateish,
    super_sector: z.string().optional(),
    major_products: z.array(z.string()).default([]),
    major_clusters: z.array(z.string()).default([]),
    major_cities: z.array(z.string()).default([]),
    related: z.array(z.string()).default([]),
  }),
});

const cities = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../content/cities' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    entity_id: z.string(),
    type: z.string(),
    slug: z.string(),
    status: z.string().optional(),
    date: dateish,
    last_verified: dateish,
    province: z.string().optional(),
    major_products: z.array(z.string()).default([]),
    major_industries: z.array(z.string()).default([]),
    major_clusters: z.array(z.string()).default([]),
    related: z.array(z.string()).default([]),
  }),
});

export const collections = { clusters, products, industries, cities };
