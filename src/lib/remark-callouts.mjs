/**
 * GitHub-style callout boxes in Markdown:
 *   > [!definition] Proposition     > [!theorem] De Morgan's laws
 *   > [!example]  > [!why]  > [!industry]  > [!warning]  > [!note]  > [!try]  > [!tip]
 * The first line may carry a title after the marker; otherwise the default label is used.
 */
const KINDS = {
  note: { label: 'Note', cls: 'callout-note' },
  tip: { label: 'Tip', cls: 'callout-note' },
  warning: { label: 'Careful', cls: 'callout-warn' },
  example: { label: 'Example', cls: 'callout-example' },
  why: { label: 'Why it matters', cls: 'callout-why' },
  industry: { label: 'In the real world', cls: 'callout-where' },
  definition: { label: 'Definition', cls: 'callout-def' },
  theorem: { label: 'Theorem', cls: 'callout-thm' },
  try: { label: 'Try it', cls: 'callout-try' },
};

const RE = /^\[!(\w+)\]\s*(.*)$/;

function visit(node, fn) {
  if (!node || typeof node !== 'object') return;
  fn(node);
  if (Array.isArray(node.children)) node.children.forEach((c) => visit(c, fn));
}

export default function remarkCallouts() {
  return (tree) => {
    visit(tree, (node) => {
      if (node.type !== 'blockquote' || !node.children?.length) return;
      const first = node.children[0];
      if (first.type !== 'paragraph' || !first.children?.length) return;
      const text = first.children[0];
      if (text.type !== 'text') return;
      const nl = text.value.indexOf('\n');
      const firstLine = nl === -1 ? text.value : text.value.slice(0, nl);
      const m = firstLine.match(RE);
      if (!m) return;
      const kind = KINDS[m[1].toLowerCase()];
      if (!kind) return;
      const title = m[2].trim() || kind.label;
      // ilk satırı kaldır
      text.value = nl === -1 ? '' : text.value.slice(nl + 1);
      if (!text.value) first.children.shift();
      if (!first.children.length) node.children.shift();

      node.data = node.data || {};
      node.data.hName = 'aside';
      node.data.hProperties = { className: ['callout', kind.cls], role: 'note' };
      node.children.unshift({
        type: 'paragraph',
        data: { hName: 'p', hProperties: { className: ['callout-title'] } },
        children: [{ type: 'text', value: title }],
      });
    });
  };
}
