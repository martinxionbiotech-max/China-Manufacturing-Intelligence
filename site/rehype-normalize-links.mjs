// Rehype plugin: normalize internal city links.
// Body content was authored with `/cities/<slug>/` links; the site routes cities
// under `/manufacturing-cities/<slug>/` (per the phase roadmap). Rewrite the
// prefix so internal links resolve to real pages.
function walk(node) {
  if (!node) return;
  if (Array.isArray(node)) {
    for (const n of node) walk(n);
    return;
  }
  if (
    node.type === 'element' &&
    node.tagName === 'a' &&
    node.properties &&
    typeof node.properties.href === 'string'
  ) {
    node.properties.href = node.properties.href.replace(
      /^\/cities\//,
      '/manufacturing-cities/',
    );
  }
  if (Array.isArray(node.children)) walk(node.children);
}

export function normalizeCityLinks() {
  return (tree) => {
    walk(tree);
  };
}
