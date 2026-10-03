/**
 * Links that leave the site open in a new tab: every http(s) link in Markdown/MDX content
 * gets target="_blank" rel="noopener noreferrer". Links to the course site itself stay in the same tab.
 */
export default function rehypeExternalLinks({ site = '' } = {}) {
  const own = site.replace(/\/$/, '');
  const visit = (node) => {
    if (node.type === 'element' && node.tagName === 'a') {
      const href = node.properties?.href;
      if (typeof href === 'string' && /^https?:\/\//.test(href) && !(own && href.startsWith(own))) {
        node.properties.target = '_blank';
        node.properties.rel = ['noopener', 'noreferrer'];
      }
    }
    node.children?.forEach(visit);
  };
  return (tree) => visit(tree);
}
